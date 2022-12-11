

#Import Libraries and Define Auxiliary Functions
#We will import the following libraries.

# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

##Data Analysis¶
##Load Space X dataset, from last section.

df=pd.read_csv("C:/Users/Louiso/Documents/03 C Programing/Data Science for python/Coursera/Capstone project/dataset_part_1.csv")
df.head(10)

##Identify and calculate the percentage of the missing values in each attribute

df.isnull().sum()/df.count()*100

##Identify which columns are numerical and categorical:

df.dtypes


# Apply value_counts() on column LaunchSite
df['LaunchSite'].value_counts()


#TASK 2: Calculate the number and occurrence of each orbit
#Use the method .value_counts() to determine the number and occurrence of each orbit in the column Orbit

# Apply value_counts on Orbit column
df['Orbit'].value_counts()


##TASK 3: Calculate the number and occurence of mission outcome per orbit type¶
##Use the method .value_counts() on the column Outcome to determine the number of landing_outcomes.Then assign it to a variable landing_outcomes.

# landing_outcomes = values on Outcome column
#df.rename(columns={'Outcome': 'landing_outcomes'}, inplace = True)
landing_outcomes = df['Outcome'].value_counts()
landing_outcomes


for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)

#We create a set of outcomes where the second stage did not land successfully:

bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
bad_outcomes


##TASK 4: Create a landing outcome label from Outcome column¶
##Using the Outcome, create a list where the element is zero if the corresponding row in Outcome is in the set bad_outcome; otherwise, it's one. Then assign it to the variable landing_class:

# landing_class = 0 if bad_outcome
# landing_class = 1 otherwise
landing_class = []
​
​
        
x = len(df['Outcome'])
for y in range(0, (x)):
    if df['Outcome'][y] in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)
landing_class


#This variable will represent the classification variable that represents the outcome of each launch. If the value is zero, the first stage did not land successfully; one means the first stage landed Successfully

df['Class']=landing_class
df[['Class']].head(8)


df.head(5)

#We can use the following line of code to determine the success rate:
df["Class"].mean()

df.to_csv("dataset_part_2.csv", index=False)


