#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
It is function to scrape the UKBiobank website:
    1) It helps you find intersection between variables available through your 
    application and (almost) all other UKB variables. 
    2) It can act as a dictionary, you can pass a variable Field ID and it will
    return the variable name and its category (by category I mean *UKbiobank* 
    pre-defined categories.)
    
    To kick start do the following:
        import UKBscrape as ukbs
        ukbs.update()
        
    You need to be connected to internet for ukbs.update() to work. Once you 
    have done it, there is a new sub-directory ~/IDLabCat which contains 
    scrapped text files from the UKBiobank. 
    
    See usage/help for individual functions. 

Created on Mon Jan  7 14:32:45 2019
@author: sorooshafyouni
University of Oxford, 2019
srafyouni@gmail.com
"""
################################################################################################
################################################################################################
import re
import numpy as np
import os 
import pandas as pd   

def update(): 
    """
    REQUIREMENTS:
    packages: os
    
    This function uses inner bash script 'UKBscrape.sh' to scrape UKBB website. 
    Need to be called on regularly bases to be updated with the latest version 
    of variables. 
    
    SA, Ox, 2019
    srafyouni@gmail.com
    """

    import os 
    
    if not os.path.isdir("IDLabCat"):
        os.makedirs('IDLabCat')
    
    os.system('sh UKBscrape.sh')
    print('==DONE UPDATES==')
    return

################################################################################################
################################################################################################
def match(UKBCSVFile = 'ukb25120_Headers.txt',\
          Report2 = ''):
    """
    ukbs.match(UKBCSVFile = '',Report2 = '')
    
    REQUIREMENTS:
        packages: os, re, numpy
        
    INPUTS:
        UKBCSVFile: path to a text file which contains *your* UKBiobank headers. 
        On you linux/Mac terminal do as following to make such file:
            $ head -n 1 /path/2/your/UKB/ukbXXXXX.csv > ukbXXXX_Headers.txt
            
       Report2 [optional]: if you need to save the reports, set a path for the results. 
       This will produce two csv files: 
           YouDontHave.csv, FieldID, label and category of the variables that you don't have
           WasntParsed.csv, the variables that may have missed in parsing but your application has! 
           
     SA, Ox, 2019      
     srafyouni@gmail.com
    """
# 1) Should check the match folder, it creates a dictory a / before the target
# 2) Also, skip if the field doesn't exist in the UKB scrapped.    
    
#######INPUT CHECK ##############    
    if UKBCSVFile == '':
        print('HALTED: Specify the path to your UKBB CSV file...')
        return
    
    if not os.path.isdir("IDLabCat"):
        update()
        
    print('You requested a match between your current version of UKBB variables at:\n'\
          + str(UKBCSVFile) + ' \n and the UKB available data at:\nhttps://biobank.ctsu.ox.ac.uk/crystal/list.cgi')
################################ 
# Extract what we have:    
    #UKBCSVFile     = 'ukb25120_Headers.txt';
    ScrapedCSVFile = 'IDLabCat/IDs_All.txt';
    WeHave = open(UKBCSVFile, 'r').read()
    A = WeHave.split(sep=',');
    
    IDRegEx = '^\"([0-9]*).*\"'
    IDsWeHave = list()
    for i in range(0,np.size(A)):
        IDsWeHave.append(re.findall(IDRegEx,A[i])[0])
        
    del IDsWeHave[0] # because the first element is always eid, right?
    
    IDsWeHave = list(set(IDsWeHave))
################################ 
    
    UKBHave = open(ScrapedCSVFile, 'r').read()
    IDsUKBHave = UKBHave.split(sep='\n')
    
    WhatWeDontHave  = list(set(IDsUKBHave)-set(IDsWeHave))
    WhatUKBDontHave = list(set(IDsWeHave)-set(IDsUKBHave))
    
    if Report2!='':
        Report2_dir = os.path.dirname(Report2)
        
        Report2_dir = Report2_dir + '/matchreport/';
        
        dictionary(UKBCSVFile=UKBCSVFile, FieldID = WhatWeDontHave, SaveMe2=Report2_dir  + 'YouDontHave.csv')
        dictionary(UKBCSVFile=UKBCSVFile, FieldID = WhatUKBDontHave, SaveMe2=Report2_dir  + 'WasntParsed.csv')
    
    return WhatWeDontHave,WhatUKBDontHave

################################################################################################
################################################################################################

def dictionary(\
              UKBCSVFile = 'ukb25120_Headers.txt',\
              FieldID = '',\
              SaveMe2 = ''):         
    """
    ukbs.dictionary(UKBCSVFile = '', FieldID = '' ,SaveMe2 = '')
    
    REQUIREMENTS:
        packages: os, numpy, pandas
        
    INPUTS:
        UKBCSVFile: path to a text file which contains *your* UKBiobank headers. 
        On you linux/Mac terminal do as following to make such file:
            $ head -n 1 /path/2/your/UKB/ukbXXXXX.csv > ukbXXXX_Headers.txt
            
        FieldID: Field IDs as a list of strings. 
            For example, labels and categories for field IDs 4056 & 26412 can be found as following:
                In [80]: ukbs.dictionary(UKBCSVFile = 'ukb25120_Headers.txt',FieldID=['4056','26412']);
                You requested dictionary for 2 data fields.
                                            Label                         Category
                4056         Age stroke diagnosed               Medical conditions
                26412  Employment score (England)  Indices of Multiple Deprivation
                     
       SaveMe2 [optional]: path to a directory to save the results as tsv file.
           saves the FieldID, labels and categories of passed FieldIDs
           
     SA, Ox, 2019      
     srafyouni@gmail.com
    """    
    
#######INPUT CHECK ##############
    if FieldID=='':
        print('HALTED: You have to specify which data field you need...')
        return
    
    headPath, tailName = os.path.split(UKBCSVFile)
    if headPath != '':
        headPath = headPath + '/'
    print("I am looking at this directory: " + headPath)    
    
    if not os.path.isdir(headPath + "IDLabCat"):
        update()
    
    print('You requested dictionary for ' + str(np.size(FieldID)) + ' data fields.')
################################
    
    DataDict = pd.DataFrame(index=FieldID,columns=('Label','Category','WeHave'))
        
    # Can't I just simply use np.loadtxt?!
    ScrapedCSVFile = headPath + 'IDLabCat/IDs_All.txt';
    UKBHave = open(ScrapedCSVFile, 'r').read()
    IDsUKBHave = UKBHave.split(sep='\n')

    Path2CatFile = headPath + 'IDLabCat/Cats_All.txt'
    CatFile = open(Path2CatFile, 'r').read()
    Cats = CatFile.split(sep='\n')

    Path2LabelFile = headPath + 'IDLabCat/Labels_All.txt'
    LabFile = open(Path2LabelFile, 'r').read()
    Labs = LabFile.split(sep='\n')
    
    for i in range(0,np.size(FieldID)):
        WeHaveFlag = False
        if not (FieldID[i] in IDsUKBHave):
            print('*****Field ID: ' + str(FieldID[i]) + ' is missing in the UKBB scrapped files.*****')
            Cats_tmp = np.nan
            Labs_tmp = np.nan
        else:
            Idx = IDsUKBHave.index(FieldID[i])            
            Cats_tmp = Cats[Idx]
            Labs_tmp = Labs[Idx]
            
            ################################ 
            # Extract what we have:    
            #UKBCSVFile     = 'ukb25120_Headers.txt';
            ScrapedCSVFile = headPath + 'IDLabCat/IDs_All.txt';
            WeHave = open(UKBCSVFile, 'r').read()
            A = WeHave.split(sep=',');
                
            IDRegEx = '^\"([0-9]*).*\"'
            IDsWeHave = list()
            for ii in range(0,np.size(A)):
                IDsWeHave.append(re.findall(IDRegEx,A[ii])[0])
                    
            del IDsWeHave[0] # because the first element is always eid, right?
                
            IDsWeHave = list(set(IDsWeHave))
            ################################ 
            if FieldID[i] in IDsWeHave:
                WeHaveFlag = True
        
        DataDict['Category'][i] = Cats_tmp 
        DataDict['Label'][i]    = Labs_tmp
        DataDict['WeHave'][i]   = WeHaveFlag
        
    print(DataDict)    
    if SaveMe2!='':
        if not os.path.isdir(SaveMe2):
            print('Report dictory was created: ' + str(SaveMe2))
            SaveMe2_dir = os.path.dirname(SaveMe2)
            os.makedirs(SaveMe2_dir,exist_ok=True)
        DataDict.to_csv(SaveMe2)
        
    return DataDict      