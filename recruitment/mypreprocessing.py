import pandas as pd
from sklearn.externals import joblib
import re
import PyPDF2 

posts = {
    0: 'Advocate',
    1: 'Arts',
    2: 'Automation Testing',
    3: 'Blockchain',
    4: 'Business Analyst',
    5: 'Civil Engineer',
    6: 'Data scientist',
    7: 'Database',
    8: 'Dev-ops Engineer',
    9: 'DotNet Developer',
    10: 'ATL Developer' ,
    11: 'Electrical Engineering',
    12: 'HR',
    13: 'Hadoop',
    14: 'Health and Fitness',
    15: 'Java Developer',
    16: 'Mechanical Engineer',
    17: 'Network Security Engineer',
    18: 'Operations Manager',
    19: 'PMO',
    20: 'Python Developer',
    21: 'SAP Developer',
    22: 'Sales',
    23: 'Testing',
    24: 'Web Designing'
}


def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText
def preprocessing(input_text):
    df = pd.DataFrame({"text":[input_text]})
    df2 = pd.DataFrame()
    df2['text'] = df.text.apply(lambda x: cleanResume(x))
    reqText = df2['text'].values
    # Load the model from the file 
    apnamodel = joblib.load('./recruitment/apnamodel.pkl')  
    apnavectorizer = joblib.load('./recruitment/apnavectorizer.pickle')

    copy_word_features = apnavectorizer.transform(reqText)

    # Use the loaded model to make predictions 
    apnapred = apnamodel.predict(copy_word_features)

    return (posts[apnapred[0]])