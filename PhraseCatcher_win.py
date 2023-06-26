# In windows powershell
# EAE Keywords Matcher code
# For EXAM Mgr/Exec applicants,
# it takes about ? min to run the prog in Python3 shell.


#importing all required libraries

import PyPDF2
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
import pandas as pd
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher

#Function to read resumes from the folder one by one
# mypath="/home/david/PY310v/Resume_EX/NLP_Resume/EXapp" #enter your path here where you saved the resumes
mypath="D:\PythonC\ResumeEX\EXapp" #enter your path here where you saved the resumes
onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

def pdfextract(file):
    fileReader = PyPDF2.PdfReader(open(file,'rb'))
    countpage = len(fileReader.pages)
    count = 0
    text = []
    while count < countpage:    
        pageObj = fileReader.pages[count]
        count +=1
        t = pageObj.extract_text()
        print (t)
        text.append(t)
    return text

#function to read resume ends


#function that does keyword(s) matching and builds a candidate profile
def create_profile(file):
    text = pdfextract(file) 
    text = str(text)
    #text = text.replace("\\n", "")
    text = text.lower()
    #below is the csv where we have all the keywords, you can customize your own
    #keyword_dict = pd.read_csv('D:\PythonC\ResumeEX\template.csv', encoding='ISO-8859-1')
    keyword_dict = pd.read_csv("D:/PythonC/ResumeEX/template.csv", encoding="ISO-8859-1")
    A_words = [nlp(text) for text in keyword_dict['Exam'].dropna(axis = 0)]
    B_words = [nlp(text) for text in keyword_dict['Graduation'].dropna(axis = 0)]
    #C_words = [nlp(text) for text in keyword_dict['Finance'].dropna(axis = 0)]
    #D_words = [nlp(text) for text in keyword_dict['Admin'].dropna(axis = 0)]
    #E_words = [nlp(text) for text in keyword_dict['Team'].dropna(axis = 0)]
    
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('Exam', None, *A_words)
    matcher.add('Grad', None, *B_words)
    #matcher.add('FIN', None, *C_words)
    #matcher.add('Admin', None, *D_words)
    #matcher.add('Team', None, *E_words)
    doc = nlp(text)
    
    d = []  
    matches = matcher(doc)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start : end]  # get the matched slice of the doc
        d.append((rule_id, span.text))      
    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())
    
    ## converting string of keywords to dataframe
    df = pd.read_csv(StringIO(keywords),names = ['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ',n=1).tolist(),columns = ['Subject','Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(',n=1).tolist(),columns = ['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1) 
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
    
    base = os.path.basename(file)
    filename = os.path.splitext(base)[0]
       
    name = filename.split('_')
    name2 = name[0]
    name2 = name2.lower()

    ## converting str to dataframe
    name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])
    
    dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis = 1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)

    return(dataf)
        
#function ends
        
#code to execute/call the above functions

final_database=pd.DataFrame()
i = 0 
while i < len(onlyfiles):
    file = onlyfiles[i]
    dat = create_profile(file)
    final_database = pd.concat([final_database, dat], ignore_index=True)
    i +=1
    print(final_database)

    
#code to count words under each category and visulaize it through Matplotlib
final_database2 = final_database['Keyword'].groupby([final_database['Candidate Name'], final_database['Subject']]).count().unstack()
final_database2.reset_index(inplace = True)
final_database2.fillna(0,inplace=True)
new_data = final_database2.iloc[:,1:]
new_data.index = final_database2['Candidate Name']

#execute the below line to see the candidate profile in a csv format
sample2=new_data.to_csv('D:/PythonC/ResumeEX/EXselect_attr.csv')

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 10})
ax = new_data.plot.barh(title="EXapp keywords by category", legend=False, figsize=(25,7), stacked=True)
labels = []
for j in new_data.columns:
    for i in new_data.index:
        label = str(j)+": " + str(new_data.loc[i][j])
        labels.append(label)
patches = ax.patches
for label, rect in zip(labels, patches):
    width = rect.get_width()
    if width > 0:
        x = rect.get_x()
        y = rect.get_y()
        height = rect.get_height()
        ax.text(x + width/2., y + height/2., label, ha='center', va='center')
plt.show()
