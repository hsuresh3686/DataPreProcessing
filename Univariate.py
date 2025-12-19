import pandas as pd
import numpy as np

class CentralTendency():
    
    def quanQual(dataset):
        quan=[];qual=[];
        for col in dataset.columns:
            if dataset[col].dtypes == "O":
                qual.append(col)
            else:
                quan.append(col)
        print("Quantative Columns : ", quan)
        print("\nQualitative Columns :", qual)
        return quan,qual
    
    def Univariate(quan,dataset):
        descriptive=pd.DataFrame(index=['Mean','Median','Mode',"Q1:25%", "Q2:50%", "Q3:75%","99%","Q4:100%","IQR","1.5Rule",
                                   "Lesser","Greater","min","max","Kurtosis","Skew"],columns=quan)
        for cols in quan:
            descriptive[cols]['Mean']=dataset[cols].mean()
            descriptive[cols]['Median']=dataset[cols].median()
            descriptive[cols]['Mode']=dataset[cols].mode()[0]
            descriptive[cols]['Q1:25%']=dataset.describe()[cols]["25%"]
            descriptive[cols]['Q2:50%']=dataset.describe()[cols]["50%"]
            descriptive[cols]['Q3:75%']=dataset.describe()[cols]["75%"]
            descriptive[cols]['99%']=np.percentile(dataset[cols],99)    #Calculating 99th Percentile
            descriptive[cols]['Q4:100%']=dataset.describe()[cols]["max"]
            descriptive[cols]['IQR']=descriptive[cols]['Q3:75%']-descriptive[cols]['Q1:25%']
            descriptive[cols]['1.5Rule']=1.5 * descriptive[cols]['IQR']
            descriptive[cols]['Lesser']=descriptive[cols]['Q1:25%'] - descriptive[cols]['1.5Rule']
            descriptive[cols]['Greater']=descriptive[cols]['Q3:75%'] + descriptive[cols]['1.5Rule']
            #descriptive[cols]['min']=dataset.describe()[cols]["min"]
            #descriptive[cols]['max']=dataset.describe()[cols]["max"]
            descriptive[cols]['min']=dataset[cols].min()
            descriptive[cols]['max']=dataset[cols].max()
            descriptive[cols]['Kurtosis']=dataset[cols].kurtosis()
            descriptive[cols]['Skew']=dataset[cols].skew()
        #print(descriptive)
        return descriptive
    
    def findOutliers(descriptive):
        Lesser,Greater=[],[]
        for column in descriptive.columns:
            if descriptive[column]['min'] < descriptive[column]['Lesser']:
                Lesser.append(column)
                #print(column)
            if descriptive[column]['max'] > descriptive[column]['Greater']:
                Greater.append(column)
                #print(column)
        print("Lesser Outliers Columns : ", Lesser)
        print("\nGreater Outliers Columns : ",Greater)    
        return Lesser,Greater 

    def fillingOutliers(Lesser,Greater,dataset,descriptive):
        Lesser=Lesser;Greater=Greater;dataset=dataset;descriptive=descriptive;
        for col in Lesser:
            dataset[col][dataset[col]<descriptive[col]["Lesser"]]=descriptive[col]["Lesser"]
        for col in Greater:
            dataset[col][dataset[col]>descriptive[col]["Greater"]]=descriptive[col]["Greater"]
    
    def freqtable(col,dataset):
        freqTable=pd.DataFrame(columns=["Unique_Values","Frequency","Relative_Frequency","Cumulative"])
        freqTable['Unique_Values']=dataset[col].value_counts().index
        freqTable['Frequency']=dataset[col].value_counts().values
        freqTable['Relative_Frequency']=freqTable['Frequency']/103
        freqTable['Cumulative']=freqTable['Relative_Frequency'].cumsum()
        
        print(freqTable)
        return freqTable