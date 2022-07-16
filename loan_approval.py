# -*- coding: utf-8 -*-
"""Loan_Approval.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d4B8GV0bmJwu9XE9RFDdH5fb3X9JodUy

# Loan Approval Prediction 

This is a binary classification problem, here we are predicting whether a person gets loan from a bank or not by taking some details of the person. 
Here we test various models but finally takes a model which gives us more accuracy.

## Importing Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
# %matplotlib inline 
import io
import plotly.express as px

import plotly.express as px
import plotly.figure_factory as ff
import plotly

from sklearn.utils import resample
from sklearn.preprocessing import StandardScaler , MinMaxScaler
from collections import Counter

#Classifiers
from sklearn.ensemble import AdaBoostClassifier , GradientBoostingClassifier , VotingClassifier , RandomForestClassifier
from sklearn.linear_model import LogisticRegression , RidgeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier 
from sklearn.naive_bayes import GaussianNB
from xgboost import plot_importance
from xgboost import XGBClassifier
from sklearn.svm import SVC

#Model evaluation tools
from sklearn.metrics import classification_report , accuracy_score , confusion_matrix
from sklearn.metrics import accuracy_score,f1_score
from sklearn.model_selection import cross_val_score

#Data processing functions
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()


from google.colab import data_table
data_table.enable_dataframe_formatter()

import warnings
warnings.filterwarnings("ignore")

"""## Uploading Data

Loading the data
"""

from google.colab import files
 
uploaded = files.upload()
df = pd.read_csv(io.BytesIO(uploaded['loan.csv']))

"""## Data Analysing 

Lets analyse the data by plotting the graphs knowing number of rows number of missing values and knowing the relationship between the variables 
"""

print(len(df))

sns.countplot("Loan_Status",data = df)

sns.countplot('Loan_Status',hue = 'Gender',data = df)

sns.countplot('Loan_Status',hue = 'Married',data = df)

sns.countplot('Loan_Status',hue = 'Education',data = df)

sns.countplot('Loan_Status',hue = 'Property_Area',data = df)

sns.countplot('Loan_Status',hue = 'Credit_History',data = df)

sns.countplot('Loan_Status',hue = 'Dependents',data = df)

sns.countplot('Loan_Status',hue = 'Self_Employed',data = df)

df.info()

sns.heatmap(df.corr(), annot=True)

df.describe()

sns.pairplot(df)

"""We can see that there are outliers in the datset 

Outliers are the values that look different from the other values in the data. Below is a plot highlighting the outliers in ‘red’ and outliers can be seen in both the extremes of data. Outliers in the data may causes problems during model fitting. Outliers may inflate the error metrics which give higher weights to large errors.

Here Outliers are present in labels ApplicantIncome and CoapplicantIncome, there are outliers in the categorical labels tooo

##Normalisation 
Central limit theorem In simple language we can say that maximum amount of data or maximum number of data points are near the Mean of the all data points.
To validate he normal distribution of the data:- Mean Mode Median are Equal.
We can gen identified the distribution of entire data with the help of Mean and Standard Deviation. When the data is normally distributed maximum data is centralized near the mean value of the data. To get understanding of distribtuion we can simply plot Distribution plot i.e. Simple Histogram.
Normally Distributed data represents a Bell Shaped curve. Also Mean, Mode , Median on Normaly Distributed data are equal. One more method is to calculate mean which should be 0 or near to 0 and Standard deviation 1 or near 1.  Normalization is generally required when we are dealing with attributes on a different scale, otherwise, it may lead to a dilution in the effectiveness of an important equally important attribute(on a lower scale) because of other attributes having values on a larger scale. In simple words, when multiple attributes are there but attributes have values on different scales, this may lead to poor data models while performing data mining operations. So they are normalized to bring all the attributes on the same scale.
"""

df.LoanAmount.hist()

"""This shows LoanAmount does not fit in Normal Distribution """

df.CoapplicantIncome.hist()

df.ApplicantIncome.hist()

"""So after observing the graphs we have concluded that we need to normalize the data as they are skewed, So for numerical labels we normalize that column

## Data Wrangling 

Here we prepare the data for modeling that is normalise the data, filling the null values, removing the outliers, removing skewness
"""

df.isnull().sum()

sns.heatmap(df.isnull())

"""So if we look the above graph we can see that there are some missing values in the data, so we need to either impute the data or just drop the rows which have null/na values but if we do that we will loose a lot of data and also with less data model which we obtain will be robust, so we will try to impute those that is replace null/na with a value.

If we see in the data we have two types of labels one is numerical and the other is categorical. There are many ways of imputing, we can either replace the null/na values with the mean value of that column or mode of that column but this does not make any sense for categorical labels, so for categorical labels we replace it with most frequent value in that column or this also makes sense that filling the value of next row in that corresponding column.

### Categorical Labels

Here we are filling the values of the categorical labels and we fill it by the most frequently occurred value in that column because they are ordinal not numerical
"""

df["Gender"].fillna(df["Gender"].mode()[0],inplace=True)
df["Married"].fillna(df["Married"].mode()[0],inplace=True)
df["Self_Employed"].fillna(df["Self_Employed"].mode()[0],inplace=True)
df["Loan_Amount_Term"].fillna(df["Loan_Amount_Term"].mode()[0],inplace=True)
df["Dependents"].fillna(df["Dependents"].mode()[0],inplace=True)
df["Credit_History"].fillna(df["Credit_History"].mode()[0],inplace=True)

#All values of "Dependents" columns were of "str" form now converting to "int" form.
df["Dependents"] = df["Dependents"].replace('3+',int(3))
df["Dependents"] = df["Dependents"].replace('1',int(1))
df["Dependents"] = df["Dependents"].replace('2',int(2))
df["Dependents"] = df["Dependents"].replace('0',int(0))

# for numerical label replacing with the mean

df["LoanAmount"].fillna(df["LoanAmount"].mean(),inplace=True)

# check out for median tooo

df.isnull().sum()

sns.heatmap(df.isnull())

"""We can see that there are no null values in the data set right now

Now normalising the data
"""

df["ApplicantIncome"] = np.log(df["ApplicantIncome"])
#As "CoapplicantIncome" columns has some "0" values we will get log values except "0"
df["CoapplicantIncome"] = [np.log(i) if i!=0 else 0 for i in df["CoapplicantIncome"]]
df["LoanAmount"] = np.log(df["LoanAmount"])

"""If we see we have a lot of string values, so we have to convert them into categorical values in order to implement the logistic regression, so we convert the strings into some categorical variables(dummy variables), which can be done using pandas, while doing ML we have to take care of strings, from strings we can not predict anything so we have to encode the strings which we have done now """

df["Gender"] = le.fit_transform(df["Gender"])
df["Married"] = le.fit_transform(df["Married"])
df["Education"] = le.fit_transform(df["Education"])
df["Self_Employed"] = le.fit_transform(df["Self_Employed"])
df["Property_Area"] = le.fit_transform(df["Property_Area"])
df["Loan_Status"] = le.fit_transform(df["Loan_Status"])

df.drop("Loan_ID", axis =1)
df.head()

dependents = df["Dependents"]
print(dependents)

"""Now the data is normalised and also strings are encoded now the data is ready for training the model

## Feature Importance

In order to create best predictive model we need to best understand the available data and get most information from the data. In multivariate data it is important to understand the importance of varialbes and how much they are contributing towards the target variable. Such that we can remove unnecessary variables to increase model performance. Many times dataset consists of extra columns which do not identically serve information to classify the data. This leads in wrong assumption of model while training. To understand the importance of the data we are going to use Machine Learning classifiers and then will plot bar graph based on importance. Also XGBoost has built-in feature importance plotting tool which we are going to use. Using more than one classifier will increase the confidence on our assumption of which variables to keep and which to remove.
"""

#Dividing data into Input X variables and Target Y variable
X = df.drop(["Loan_Status","Loan_ID"],axis=1)
y = df["Loan_Status"]

print("Feature importance by XGBoost:\n")
XGBR = XGBClassifier()
XGBR.fit(X,y)
features = XGBR.feature_importances_
Columns = list(X.columns)
for i,j in enumerate(features):
    print(Columns[i],":",j)
    print("\n")
plt.figure(figsize=(16,5))
plt.title(label="XGBC")
plt.bar([x for x in range(len(features))],features)
plt.show()

plot_importance(XGBR)

print("Feature importance by Random Forest:\n")
RF = RandomForestClassifier()
RF.fit(X,y)
features = RF.feature_importances_
Columns = list(X.columns)
for i,j in enumerate(features):
    print(Columns[i],"->",j)
    print("\n")
plt.figure(figsize=(16,5))
plt.title(label="RF")
plt.bar([x for x in range(len(features))],features)
plt.show()

print("Feature importance by Decision Tree:\n")
DT = DecisionTreeClassifier()
DT.fit(X,y)
features = DT.feature_importances_
Columns = list(X.columns)
for i,j in enumerate(features):
    print(Columns[i],":",j)
    print("\n")
plt.figure(figsize=(16,5))
plt.title(label="DT")
plt.bar([x for x in range(len(features))],features)
plt.show()

print("Feature importance by Suppoprt Vector Machine:\n")
SVM = SVC(kernel="linear")
SVM.fit(X,y)
features = SVM.coef_[0]
Columns = list(X.columns)
for i,j in enumerate(features):
    print(Columns[i],":",j)
    print("\n")
plt.figure(figsize=(16,5))
plt.bar([x for x in range(len(features))],features)
plt.show()

print("Feature importance by Logistic Regression:\n")
LOGC = LogisticRegression()
LOGC.fit(X,y)
features = LOGC.coef_[0]
Columns = list(X.columns)
for i,j in enumerate(features):
    print(Columns[i],":",j)
    print("\n")
plt.figure(figsize=(16,5))
plt.title(label="LOGC")
plt.bar([x for x in range(len(features))],features)
plt.show()

"""So from the feature importance we can see that Credit History, ApplicantIncome, CoapplicantIncome, LoanAmount are the most important features"""

#Heat map of dataset with relative importance
matrix = df.drop(["Gender","Married","Dependents","Education","Self_Employed"],axis=1).corr()


plt.figure(figsize=(18,8))
sns.heatmap(matrix,vmax=0.8,square=True,cmap="BuPu", annot = True)

"""It seems Application income and Loan Amount is correlated , also Coapplication income correlated with Loan Aount then Credit history is corrleated with Loan Status"""

A = list(df.Loan_Status).count(1)
B = list(df.Loan_Status).count(0)
print("Count of 1 (Approved) : ",A,"\nCount of 0 (Rejected) : ",B)

"""It seems that data is highly Imbalanced. When the target classes does not have equal count then the data is considered as imbalanced data. From above graph it seems that dataset contains more records with Approved Loan_Status than Rejected Loan_Status. 422 over 192 If data would have maximum of 20-30 records difference that time this imabalnced would be ignorable. Which will lead to make wrong assumptions by model and also model will be biased after training. We will overcome this issue by balancing the data. To overcome this problem we will balance the data using resampling technique with Upsample and Downsample."""

data = df.copy()
data.head()

#Getting seperated data with 1 and 0 status.
df_majority = data[data.Loan_Status==1]
df_minority = data[data.Loan_Status==0]

#Here we are downsampling the Majority Class Data Points. 
#i.e. We will get equal amount of datapoint as Minority class from Majority class

df_majority_downsampled = resample(df_majority,replace=False,n_samples=192,random_state=123)
df_downsampled = pd.concat([df_majority_downsampled,df_minority])
print("Downsampled data: \n",df_downsampled.Loan_Status.value_counts())
print("\n")
#Here we are upsampling the Minority Class Data Points. 
#i.e. We will get equal amount of datapoint as Majority class from Minority class
df_minority_upsampled = resample(df_minority,replace=True,n_samples=422,random_state=123)
df_upsampled = pd.concat([df_majority,df_minority_upsampled])
print("Upsampled data: \n",df_upsampled.Loan_Status.value_counts())

"""## Modeling 

In order to gain maximum posible accuracy one needs to conduct more experiments.

We will pass data one by one with different state i.e.

-Only Scaled data

-Scaled + Down Sampled Data

-Scaled + Up Sampled Data

-Scaled + Up Sampled Data + Selected feature with respective importance.

### Experiment1 Only Scaled Data
"""

new_data = df.copy()

X = new_data.drop(["Loan_Status","Loan_ID"],axis=1)
y = new_data["Loan_Status"]

X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.25,random_state=0)

#Scaling data 

StSc = StandardScaler()
X_train  = StSc.fit_transform(X_train)
X_test  = StSc.fit_transform(X_test)

#Voting ensemble method. Combining all tree based algorithms.
models = []
models.append(("XGB",XGBClassifier()))
models.append(("RF",RandomForestClassifier()))
models.append(("DT",DecisionTreeClassifier()))
models.append(("ADB",AdaBoostClassifier()))
models.append(("GB",GradientBoostingClassifier()))

ensemble = VotingClassifier(estimators=models)
ensemble.fit(X_train,y_train)
y_pred = ensemble.predict(X_test) 
print(classification_report(y_pred,y_test))
print("Voting Ensemble: ",accuracy_score(y_pred,y_test))

SVM = SVC(kernel="linear",class_weight="balanced",probability=True)
SVM.fit(X_train,y_train)
y_pred = SVM.predict(X_test)
print(classification_report(y_pred,y_test))
print("SVM: ",accuracy_score(y_pred,y_test))

XGBC = XGBClassifier(learning_rate =0.1,n_estimators=10000,max_depth=4,min_child_weight=6,gamma=0,subsample=0.6,colsample_bytree=0.8,reg_alpha=0.005, objective= 'binary:logistic', nthread=2, scale_pos_weight=1, seed=27)
XGBC.fit(X_train,y_train)
y_pred = XGBC.predict(X_test)
print(classification_report(y_pred,y_test))
print("XGBoost: ",accuracy_score(y_pred,y_test))

Model1 = RandomForestClassifier(n_estimators=1000,random_state=0,n_jobs=1000,max_depth=70,bootstrap=True)
Model1.fit(X_train,y_train)
y_pred = Model1.predict(X_test)
print(classification_report(y_pred,y_test))
print("RandomForestClassifier: ",accuracy_score(y_pred,y_test))

Model2 = GradientBoostingClassifier()
Model2.fit(X_train,y_train)
y_pred = Model2.predict(X_test)
print(classification_report(y_pred,y_test))
print("GradientBoostingClassifier: ",accuracy_score(y_pred,y_test))

Model3 = DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=100,max_features=1.0, max_leaf_nodes=10,min_impurity_decrease=1e-07, min_samples_leaf=1,min_samples_split=2, min_weight_fraction_leaf=0.10, random_state=27, splitter='best')
Model3.fit(X_train,y_train)
y_pred = Model3.predict(X_test)
print(classification_report(y_pred,y_test))
print("DecisionTreeClassifier: ",accuracy_score(y_pred,y_test))

Model4 = AdaBoostClassifier()
Model4.fit(X_train,y_train)
y_pred = Model4.predict(X_test)
print(classification_report(y_pred,y_test))
print("AdaBoostClassifier: ",accuracy_score(y_pred,y_test))

Model5 = LinearDiscriminantAnalysis()
Model5.fit(X_train,y_train)
y_pred = Model5.predict(X_test)
print(classification_report(y_pred,y_test))
print("LinearDiscriminantAnalysis: ",accuracy_score(y_pred,y_test),"\n")

KNN = KNeighborsClassifier(leaf_size=1,p=2,n_neighbors=20)
KNN.fit(X_train,y_train)
y_pred = KNN.predict(X_test)
print(classification_report(y_pred,y_test))
print("KNeighborsClassifier: ",accuracy_score(y_pred,y_test))

Model7 = GaussianNB()
Model7.fit(X_train,y_train)
y_pred = Model7.predict(X_test)
print(classification_report(y_pred,y_test))
print("GaussianNB: ",accuracy_score(y_pred,y_test))

Model8 = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,penalty='l2', random_state=None, solver='liblinear', tol=0.0001,verbose=0, warm_start=False)
Model8.fit(X_train,y_train)
y_pred = Model8.predict(X_test)
print(classification_report(y_pred,y_test))
print("Logistic Regression: ",accuracy_score(y_pred,y_test))

"""## Experiment2 Scaled and Down Sampled Data

"""

X = df_downsampled.drop(["Loan_Status","Loan_ID"],axis=1)
y = df_downsampled.Loan_Status

X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.25,random_state=0)

#Scaling data 

StSc = StandardScaler()
X_train  = StSc.fit_transform(X_train)
X_test  = StSc.fit_transform(X_test)

models = []
models.append(("XGB",XGBClassifier()))
models.append(("RF",RandomForestClassifier()))
models.append(("DT",DecisionTreeClassifier()))
models.append(("ADB",AdaBoostClassifier()))
models.append(("GB",GradientBoostingClassifier()))

ensemble = VotingClassifier(estimators=models)
ensemble.fit(X_train,y_train)
y_pred = ensemble.predict(X_test) 
print(classification_report(y_pred,y_test))
print("Voting Ensemble: ",accuracy_score(y_pred,y_test))

SVM = SVC(kernel="linear",class_weight="balanced",probability=True)
SVM.fit(X_train,y_train)
y_pred = SVM.predict(X_test)
print(classification_report(y_pred,y_test))
print("SVM: ",accuracy_score(y_pred,y_test))

XGBC = XGBClassifier(learning_rate =0.1,n_estimators=10000,max_depth=4,min_child_weight=6,gamma=0,subsample=0.6,colsample_bytree=0.8,reg_alpha=0.005, objective= 'binary:logistic', nthread=2, scale_pos_weight=1, seed=27)
XGBC.fit(X_train,y_train)
y_pred = XGBC.predict(X_test)
print(classification_report(y_pred,y_test))
print("XGBoost: ",accuracy_score(y_pred,y_test))

Model1 = RandomForestClassifier(n_estimators=1000,random_state=0,n_jobs=1000,max_depth=70,bootstrap=True)
Model1.fit(X_train,y_train)
y_pred = Model1.predict(X_test)
print(classification_report(y_pred,y_test))
print("RandomForestClassifier: ",accuracy_score(y_pred,y_test))

Model2 = GradientBoostingClassifier()
Model2.fit(X_train,y_train)
y_pred = Model2.predict(X_test)
print(classification_report(y_pred,y_test))
print("GradientBoostingClassifier: ",accuracy_score(y_pred,y_test))

Model3 = DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=100,max_features=1.0, max_leaf_nodes=10,min_impurity_decrease=1e-07, min_samples_leaf=1,min_samples_split=2, min_weight_fraction_leaf=0.10, random_state=27, splitter='best')
Model3.fit(X_train,y_train)
y_pred = Model3.predict(X_test)
print(classification_report(y_pred,y_test))
print("DecisionTreeClassifier: ",accuracy_score(y_pred,y_test))

Model4 = AdaBoostClassifier()
Model4.fit(X_train,y_train)
y_pred = Model4.predict(X_test)
print(classification_report(y_pred,y_test))
print("AdaBoostClassifier: ",accuracy_score(y_pred,y_test))

Model5 = LinearDiscriminantAnalysis()
Model5.fit(X_train,y_train)
y_pred = Model5.predict(X_test)
print(classification_report(y_pred,y_test))
print("LinearDiscriminantAnalysis: ",accuracy_score(y_pred,y_test))

KNN = KNeighborsClassifier(leaf_size=1,p=2,n_neighbors=20)
KNN.fit(X_train,y_train)
y_pred = KNN.predict(X_test)
print(classification_report(y_pred,y_test))
print("KNeighborsClassifier: ",accuracy_score(y_pred,y_test))

Model7 = GaussianNB()
Model7.fit(X_train,y_train)
y_pred = Model7.predict(X_test)
print(classification_report(y_pred,y_test))
print("GaussianNB: ",accuracy_score(y_pred,y_test))

Model8 = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,penalty='l2', random_state=None, solver='liblinear', tol=0.0001,verbose=0, warm_start=False)
Model8.fit(X_train,y_train)
y_pred = Model8.predict(X_test)
print(classification_report(y_pred,y_test))
print("Logistic Regression: ",accuracy_score(y_pred,y_test))

"""## Experiment3 Scaled and Up Sampled Data """

X = df_upsampled.drop(["Loan_Status","Loan_ID"],axis=1)
y = df_upsampled.Loan_Status

X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.25,random_state=0)

#Scaling data 

StSc = StandardScaler()
X_train  = StSc.fit_transform(X_train)
X_test  = StSc.fit_transform(X_test)

models = []
models.append(("XGB",XGBClassifier()))
models.append(("RF",RandomForestClassifier()))
models.append(("DT",DecisionTreeClassifier()))
models.append(("ADB",AdaBoostClassifier()))
models.append(("GB",GradientBoostingClassifier()))

ensemble = VotingClassifier(estimators=models)
ensemble.fit(X_train,y_train)
y_pred = ensemble.predict(X_test) 
print(classification_report(y_pred,y_test))
print("Voting Ensemble: ",accuracy_score(y_pred,y_test))

SVM = SVC(kernel="linear",class_weight="balanced",probability=True)
SVM.fit(X_train,y_train)
y_pred = SVM.predict(X_test)
print(classification_report(y_pred,y_test))
print("SVM: ",accuracy_score(y_pred,y_test))

XGBC = XGBClassifier(learning_rate =0.1,n_estimators=10000,max_depth=4,min_child_weight=6,gamma=0,subsample=0.6,colsample_bytree=0.8,reg_alpha=0.005, objective= 'binary:logistic', nthread=2, scale_pos_weight=1, seed=27)
XGBC.fit(X_train,y_train)
y_pred = XGBC.predict(X_test)
print(classification_report(y_pred,y_test))
print("XGBoost: ",accuracy_score(y_pred,y_test))

Model1 = RandomForestClassifier(n_estimators=1000,random_state=0,n_jobs=1000,max_depth=70,bootstrap=True)
Model1.fit(X_train,y_train)
y_pred = Model1.predict(X_test)
print(classification_report(y_pred,y_test))
print("RandomForestClassifier: ",accuracy_score(y_pred,y_test))

Model2 = GradientBoostingClassifier()
Model2.fit(X_train,y_train)
y_pred = Model2.predict(X_test)
print(classification_report(y_pred,y_test))
print("GradientBoostingClassifier: ",accuracy_score(y_pred,y_test))

Model3 = DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=100,max_features=1.0, max_leaf_nodes=10,min_impurity_decrease=1e-07, min_samples_leaf=1,min_samples_split=2, min_weight_fraction_leaf=0.10, random_state=27, splitter='best')
Model3.fit(X_train,y_train)
y_pred = Model3.predict(X_test)
print(classification_report(y_pred,y_test))
print("DecisionTreeClassifier: ",accuracy_score(y_pred,y_test))

Model4 = AdaBoostClassifier()
Model4.fit(X_train,y_train)
y_pred = Model4.predict(X_test)
print(classification_report(y_pred,y_test))
print("AdaBoostClassifier: ",accuracy_score(y_pred,y_test))

Model5 = LinearDiscriminantAnalysis()
Model5.fit(X_train,y_train)
y_pred = Model5.predict(X_test)
print(classification_report(y_pred,y_test))
print("LinearDiscriminantAnalysis: ",accuracy_score(y_pred,y_test))

KNN = KNeighborsClassifier(leaf_size=1,p=2,n_neighbors=20)
KNN.fit(X_train,y_train)
y_pred = KNN.predict(X_test)
print(classification_report(y_pred,y_test))
print("KNeighborsClassifier: ",accuracy_score(y_pred,y_test))

Model7 = GaussianNB()
Model7.fit(X_train,y_train)
y_pred = Model7.predict(X_test)
print(classification_report(y_pred,y_test))
print("GaussianNB: ",accuracy_score(y_pred,y_test))

Model8 = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,penalty='l2', random_state=None, solver='liblinear', tol=0.0001,verbose=0, warm_start=False)
Model8.fit(X_train,y_train)
y_pred = Model8.predict(X_test)
print(classification_report(y_pred,y_test))
print("Logistic Regression: ",accuracy_score(y_pred,y_test))

"""## Experiment4 Scaled Data with selective features and importance of those features"""

X = new_data.drop(["Loan_ID","Gender","Married","Education","Self_Employed","Loan_Amount_Term","Loan_Status","Property_Area"],axis=1)
y = new_data.Loan_Status

X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.25,random_state=0)

#Scaling data 

StSc = StandardScaler()
X_train  = StSc.fit_transform(X_train)
X_test  = StSc.fit_transform(X_test)

models = []
models.append(("XGB",XGBClassifier()))
models.append(("RF",RandomForestClassifier()))
models.append(("DT",DecisionTreeClassifier()))
models.append(("ADB",AdaBoostClassifier()))
models.append(("GB",GradientBoostingClassifier()))

ensemble = VotingClassifier(estimators=models)
ensemble.fit(X_train,y_train)
y_pred = ensemble.predict(X_test) 
print(classification_report(y_pred,y_test))
print("Voting Ensemble: ",accuracy_score(y_pred,y_test))

SVM = SVC(kernel="linear",class_weight="balanced",probability=True)
SVM.fit(X_train,y_train)
y_pred = SVM.predict(X_test)
print(classification_report(y_pred,y_test))
print("SVM: ",accuracy_score(y_pred,y_test))

XGBC = XGBClassifier(learning_rate =0.1,n_estimators=10000,max_depth=4,min_child_weight=6,gamma=0,subsample=0.6,colsample_bytree=0.8,reg_alpha=0.005, objective= 'binary:logistic', nthread=2, scale_pos_weight=1, seed=27)
XGBC.fit(X_train,y_train)
y_pred = XGBC.predict(X_test)
print(classification_report(y_pred,y_test))
print("XGBoost: ",accuracy_score(y_pred,y_test))

Model1 = RandomForestClassifier(n_estimators=1000,random_state=0,n_jobs=1000,max_depth=70,bootstrap=True)
Model1.fit(X_train,y_train)
y_pred = Model1.predict(X_test)
print(classification_report(y_pred,y_test))
print("RandomForestClassifier: ",accuracy_score(y_pred,y_test))

Model2 = GradientBoostingClassifier()
Model2.fit(X_train,y_train)
y_pred = Model2.predict(X_test)
print(classification_report(y_pred,y_test))
print("GradientBoostingClassifier: ",accuracy_score(y_pred,y_test))

Model3 = DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=100,max_features=1.0, max_leaf_nodes=10,min_impurity_decrease=1e-07, min_samples_leaf=1,min_samples_split=2, min_weight_fraction_leaf=0.10, random_state=27, splitter='best')
Model3.fit(X_train,y_train)
y_pred = Model3.predict(X_test)
print(classification_report(y_pred,y_test))
print("DecisionTreeClassifier: ",accuracy_score(y_pred,y_test))

Model4 = AdaBoostClassifier()
Model4.fit(X_train,y_train)
y_pred = Model4.predict(X_test)
print(classification_report(y_pred,y_test))
print("AdaBoostClassifier: ",accuracy_score(y_pred,y_test))

Model5 = LinearDiscriminantAnalysis()
Model5.fit(X_train,y_train)
y_pred = Model5.predict(X_test)
print(classification_report(y_pred,y_test))
print("LinearDiscriminantAnalysis: ",accuracy_score(y_pred,y_test))

KNN = KNeighborsClassifier(leaf_size=1,p=2,n_neighbors=20)
KNN.fit(X_train,y_train)
y_pred = KNN.predict(X_test)
print(classification_report(y_pred,y_test))
print("KNeighborsClassifier: ",accuracy_score(y_pred,y_test))

Model7 = GaussianNB()
Model7.fit(X_train,y_train)
y_pred = Model7.predict(X_test)
print(classification_report(y_pred,y_test))
print("GaussianNB: ",accuracy_score(y_pred,y_test))

Model8 = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,penalty='l2', random_state=None, solver='liblinear', tol=0.0001,verbose=0, warm_start=False)
Model8.fit(X_train,y_train)
y_pred = Model8.predict(X_test)
print(classification_report(y_pred,y_test))
print("Logistic Regression: ",accuracy_score(y_pred,y_test))

"""## Tuning Support Vector Machine Parameters"""

X = new_data.drop(["Loan_Status","Loan_ID"],axis=1)
y = new_data.Loan_Status

X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.25,random_state=0)

model = SVC()
kernel = ['poly', 'rbf', 'sigmoid']
C = [50, 10, 1.0, 0.1, 0.01]
gamma = ['scale']

grid = dict(kernel=kernel,C=C,gamma=gamma)
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring='accuracy',error_score=0)
grid_result = grid_search.fit(X, y)

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

"""## Final Conclusion     


### Experiment 1 : Scaled data only

| Algorithm :                  |       Accuracy   |
|------------------------------|----------------- |
| Support Vector Machine       |       83.116     |
| Decision Tree                |       83.1168    |
| Linear Discriminant Analysis |       83.166     |
| KNearest Neighbors           |       83.766     |
| Gaussian Naivey Bayes        |       83.116     |
| Logistic Regression          |       83.116     |

### Experiment 2: Scaled + Down Sampled Data

| Algorithm :                  |       Accuracy   |
|------------------------------|----------------- |
| AdaBoost                     |       75         | 
| Decision Tree                |       72.91      |
| Support Vector Machine       |       70.8       |



### Experiment 3: Scaled + Up Sampled Data

| Algorithm :                  |       Accuracy   |
|------------------------------|----------------- |
| Random Forest                |       81.99      |

### Experiment 4: Scaled + Selected features with respective importance

| Algorithm :                  |       Accuracy   |
|------------------------------|----------------- |
| Support Vector Machine       |       83.11      |
| Decision Tree                |       83.11      |
| Adabost                      |       82.46      |
| Linear Discriminant Analysis |       83.11      |
| KNearest Neighbors           |       83.11      |
| Logistic Regression          |       83.11      |

After all possible experiments Maximum accuracy is achieved by Scaled Data by K-Nearest Neighbors

# Pickeling the Model
"""

new_data = df.copy()

new_data.head()

X = new_data.drop(["Loan_Status","Loan_ID"],axis=1)
y = new_data["Loan_Status"]

X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.25,random_state=0)

#Scaling data 

StSc = StandardScaler()
X_train  = StSc.fit_transform(X_train)
X_test  = StSc.fit_transform(X_test)

best_Loan_model = KNeighborsClassifier(leaf_size=1,p=2,n_neighbors=20)
best_Loan_model.fit(X_train,y_train)
y_pred = best_Loan_model.predict(X_test)
print(classification_report(y_pred,y_test))
print("KNeighborsClassifier: ",accuracy_score(y_pred,y_test))

import pickle
with open('loan_application.pickle','wb') as f:
    pickle.dump(best_Loan_model,f)

import json
columns = {
    'data_columns' : [col.lower() for col in X.columns]
}
with open("columns.json","w") as f:
    f.write(json.dumps(columns))

X.columns

def predict_loan_appl(LoanAmount, Loan_Amount_Term, Gender, Married, Dependents, Education, Self_Employed, 
                      Credit_History, Property_Area, ApplicantIncome=0, CoapplicantIncome=0):
    
    # Get medians of loanamount and loan_amount_term, while re-training and assign to below 2 variables.
    median_loanamount=126
    median_loan_amount_term=360
        
    LoanAmount= LoanAmount or median_loanamount
    Loan_Amount_Term = Loan_Amount_Term or median_loan_amount_term
    
    # All categorical features are defaulted to 'else' if there is NULL. Make sure Mode of each feature falls in 'ELSE' part.
    if Gender=='Female':
        g =0
    else:
        g =1
    if Married=='No':
        m =0
    else:
        m =1

    dep=Dependents
    if dep=='1':
        dp = 1
    elif dep=='2':
        dp =2
    elif dep=='3+':
        dp =3
    else:
      dp = 0 
    
    if Education=='Not Graduate':
        e =0
    else:
        e =1
    
    if Self_Employed=='Yes':
        se =1
    else:
        se =0

    if Credit_History=='0':
        ch = 0
    else:
        ch = 1
    
    prop_area=Property_Area
    if prop_area=='Rural':
        pa = 0
    elif prop_area=='Urban':
        pa = 2
    else:
        pa = 1
        
    x = np.zeros(len(X.columns))
    x[0] = g
    x[1] = m
    x[2] = dp
    x[3] = e
    x[4] = se
    x[5] = 0
    x[6] = 0
    x[7] = LoanAmount
    x[8] = Loan_Amount_Term
    x[9] = ch
    x[10] = pa
    
    return best_Loan_model.predict([x])[0]

predict_loan_appl(115, 30, 'Female', "No", '3+', 'Graduate', 'No', 'NAN', 'Urban')

predict_loan_appl(115, 30, 'Female', "No", '3+', 'Graduate', 'No', 'NAN', 'Urban')