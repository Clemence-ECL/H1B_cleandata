import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import table

df = pd.read_excel('merged_data_20000bis.xlsx')


# #Where to go to work as Computer Systems Analyst
tab_result = df.loc[(df['CASE_STATUS']=='CERTIFIED')&(df['SOC_NAME']=='Computer Systems Analysts'),
['EMPLOYER_NAME','EMPLOYER_CITY','WORKSITE_CITY']]
print(tab_result['EMPLOYER_CITY'].value_counts().max)
print(tab_result['WORKSITE_CITY'].value_counts().max)
print(tab_result['EMPLOYER_NAME'].value_counts().max)

#Low paid or high paid job
  #What is low paid or high paid job in the US ?
low_paid = df['WAGE_RATE_OF_PAY'].describe()[4]
high_paid = df['WAGE_RATE_OF_PAY'].describe()[6]

low_paid_jobs = df.loc[(df['WAGE_RATE_OF_PAY']<low_paid),['CASE_STATUS','EMPLOYER_NAME','EMPLOYER_CITY','SOC_NAME']]
high_paid_jobs = df.loc[(df['WAGE_RATE_OF_PAY']>high_paid),['CASE_STATUS','EMPLOYER_NAME','EMPLOYER_CITY','SOC_NAME']]

lp_jobs = low_paid_jobs['CASE_STATUS'].value_counts()
hp_jobs = high_paid_jobs['CASE_STATUS'].value_counts()


print(lp_jobs)
print(hp_jobs)

