# import statement
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
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
def countFrequency(doc):
    # (make it like this) takes a description from df and turn into array to run in this function 
    cv = CountVectorizer()
    doc = cv.fit_transform(doc)
    vector = pd.DataFrame(doc.toarray(), columns=cv.get_feature_names())
    return vector
def iftdf(doc):
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
        preprocessed = preprocessing(i)
        desList.append(preprocessed)
    return desList