# import statement
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity as cs
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
# Downloads the stopwords and corpus
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# why we are removing stop words and PortserStemmer
# To descrease the noise and the sample size to detect
# Help with TFIDF
def preprocessing(des):
    """Take description string and return string "sen" which is preprocessed"""
    """Helper function for getDesList"""
   
    # First remove the stop words, punctutation and Tokenizer
    wordTokens = word_tokenize(des)
    stopWords = set(stopwords.words('english'))
    # Removes the stop words
    filteredSen = [word for word in wordTokens if not word.lower() in stopWords]
    # Removes the punctutation and digit
    filteredSen = [word for word in filteredSen if word.isalnum()]
    # removes the digit
    filteredSen = [word for word in filteredSen if not word.isdigit()]
    # Removes the string which start with digit
    filteredSen = [word for word in filteredSen if not word[0].isdigit()]
    # As the description has too many word, we want to narrow the search down. So, we information after words "Qualification" and "requirement" is found
    try:
        target_index = filteredSen.index('qualification') + 1
    except ValueError:
        try:
            target_index = filteredSen.index('qualifications') + 1
        except ValueError:
            try:
                target_index = filteredSen.index('requirement') + 1
            except ValueError:
                try:
                    target_index = filteredSen.index('requirements') + 1
                except ValueError:
                    target_index = 0
                    
   
    filteredSen = filteredSen[target_index:]
    # Second PorterStemmer
    # calling the PorterStemmer function from nltk
    preprocessed = []
    psa = PorterStemmer()
    for word in filteredSen:
        preprocessed.append(psa.stem(word))
    sen = ' '.join(preprocessed)
    return sen

# Last TFIDF Algorithm
# put this in the script
# both the function below takes array
def countFrequency(df):
    doc = []
    text = " ".join(sen for sen in df.Description)
    doc.append(text)
    cv = CountVectorizer()
    doc = cv.fit_transform(doc)
    vector = pd.DataFrame(doc.toarray(), columns=cv.get_feature_names())
    return vector
def iftdf(df):
    doc = []
    text = " ".join(sen for sen in df.Description)
    doc.append(text)
    # doc -> list
    # calling the Scikit - Learn lib
    vectorizer = TfidfVectorizer()
    doc = vectorizer.fit_transform(doc)
    vector = pd.DataFrame(doc.toarray(),columns=vectorizer.get_feature_names_out())
    return vector

def getDesList(des):
    """Takes in pandas DataFrame (i.e df['Description']) and return list with all the job description which is also preprocessed"""
    """later used to calculate iftdf and count Frequency"""
    desList = []
    for i in des:
        desList.append(i)
    return desList

def wCloud(df):
    text = " ".join(sen for sen in df.Description)
    wordcloud = WordCloud(width= 1200, height = 800, background_color="white").generate(text)
    plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def searchHardSkills(df):
    """Take pandas count frequency and idtdf and return pandas with relevant hard skills"""
    # listen of generalized hard skill between 5 jobs
    hardSkills = ['php', 'javascript', 'python', 'java', 'react', 'js', 'angular', 'vue.js', 'c', 'c++', 'sql', 'tableau', 'spark', 
    'hadoop', 'microsoft office', 'excel', 'word', 'powerpoint', 'access', 'r', 'html', 'css', 'git', 'powerbi']
    # if these hardskills exist get the columns if not make the column value 0.
    temp = []
    for n in hardSkills:
        if n in df.columns:
            temp.append(n)

    return df[temp]

def getCosineSim(df1, df2):
    """Take in two data frame and return cosine Similarity between two data frame"""
    outerJoinDf = pd.merge(df1,df2,on="technical skills", how='outer').fillna(0)
    df1_count = outerJoinDf["count_x"].astype(int).to_list()
    arrayVec1 = np.array([df1_count])
    df2_count = outerJoinDf["count_y"].astype(int).to_list()
    arrayVec2 = np.array([df2_count])
    sim = cs(arrayVec1, arrayVec2)
    return sim
