import pandas as pd
import random
resumeDataSet = pd.read_csv('./recruitment/finaldata.csv')
def giveSearchResults(cinput, sinput):
    list_of_candidates = []
    sinput = sinput.split(',')
    for i in range(len(resumeDataSet['Category'])):
        if resumeDataSet['Category'][i]==cinput:
            for x in sinput:
                if x in resumeDataSet['Resume'][i]:
                    l = {'post': resumeDataSet['Category'][i], 'resume': resumeDataSet['Resume'][i], 'name': resumeDataSet['name'][i], 'age': random.randint
                    (25,36), 'randomno': random.randint(1,5)}
                    list_of_candidates.append(l)
    return list_of_candidates