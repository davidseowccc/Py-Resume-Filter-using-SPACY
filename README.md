# Resume-Filter-using-SPACY
Resume Filter using PyPDF2 and SPACY
1. ResumeFilter.py is based on older python version (around python 3.8 and associated pypdf2 library).
2. The other python scripts have been updated with python 3.11 and the associated pypdf2 library.

#
### Trouble-shooting
1. To install en_core_web_sm in spacy

  $ python -m spacy download en_core_web_sm

2. To a GUI backend for python3

  $ pip install pyqt5
  
  (UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.)

#
### Introduction
Resumes of Job and Study applications can become an enourmous chore of work and labourious for HR and admission/application officers to scan through without any lapse in attention and human fatique. This project makes use of programming automation to extract and read resumes with the intent of scoring and filtering applications for downstream selections. This app might be used with other HR and selection assessments.
#
#
### Objectives
The Python code, using PyPDF2 and SPACY PyPI, mines text from pdf documents using Natural Language Processing (NLP) to screen objectively thousands of resumes in a few minutes without bias to identify the best fit for a job opening based on thresholds, specific criteria or scores.
#
#
### How it works
1. Setup criterion and table of key words (set up a database using a .csv file)
2. Automatically reads resumes using PyPDF2 (you could use other libraries e.g. PDFminer.
3. Categorise Phrase/Text(s) according to the criterion and count for each applicant
4. Display Data Visualisation and Export processed data for downstream processing
#
#
#
##### References
##### 1. https://towardsdatascience.com/do-the-keywords-in-your-resume-aptly-represent-what-type-of-data-scientist-you-are-59134105ba0d
##### 2. https://towardsdatascience.com/resume-screening-with-python-1dea360be49b
