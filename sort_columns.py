import pandas as pd
import numpy as np

# Homogenisation of 2014 dataframe
df14 = pd.read_csv('data_2014.csv',index_col=0)

df14 = df14[['LCA_CASE_NUMBER', 'STATUS', 'LCA_CASE_SUBMIT', 'DECISION_DATE', 'VISA_CLASS',
'LCA_CASE_EMPLOYMENT_START_DATE', 'LCA_CASE_EMPLOYMENT_END_DATE', 'LCA_CASE_EMPLOYER_NAME',
'LCA_CASE_EMPLOYER_ADDRESS', 'LCA_CASE_EMPLOYER_CITY', 'LCA_CASE_EMPLOYER_STATE', 'LCA_CASE_EMPLOYER_POSTAL_CODE',
'LCA_CASE_JOB_TITLE','LCA_CASE_SOC_CODE', 'LCA_CASE_SOC_NAME','LCA_CASE_NAICS_CODE','TOTAL_WORKERS','FULL_TIME_POS',
'PW_1', 'PW_UNIT_1','PW_SOURCE_1','OTHER_WAGE_SOURCE_1','LCA_CASE_WAGE_RATE_FROM', 'LCA_CASE_WAGE_RATE_TO',
'LCA_CASE_WAGE_RATE_UNIT','LCA_CASE_WORKLOC1_CITY', 'LCA_CASE_WORKLOC1_STATE']]

df14.insert(9,"EMPLOYER_ADDRESS_2",np.nan)
df14.insert(13,"EMPLOYER_COUNTRY",np.nan)
df14.insert(14,"EMPLOYER_PROVINCE",np.nan)
df14.insert(15,"EMPLOYER_PHONE",np.nan)
df14.insert(16,"EMPLOYER_PHONE_EXT",np.nan)
df14.insert(17,"AGENT_ATTORNEY_NAME",np.nan)
df14.insert(18,"AGENT_ATTORNEY_CITY",np.nan)
df14.insert(19,"AGENT_ATTORNEY_STATE",np.nan)
df14.insert(28,"PW_WAGE_LEVEL",np.nan)
df14.insert(30,"PW_SOURCE_YEAR",np.nan)
df14.insert(35,"H1B_DEPENDENT",np.nan)
df14.insert(36,"WILLFUL_VIOLATOR",np.nan)
df14.insert(38,"WORKSITE_COUNTY",np.nan)
df14.insert(40,"WORKSITE_POSTAL_CODE",np.nan)
df14.insert(41,"ORIGINAL_CERT_DATE",np.nan)

# Homogenisation of 2015 dataframe
df15 = pd.read_csv('data_2015.csv',index_col=0)
df15.insert(33,"WAGE_RATE_OF_PAY_TO",np.nan)
df15["ORIGINAL_CERT_DATE"]=np.nan
columns_names = list(df15.columns.values)
print(columns_names)


# Homogenisation of 2016 dataframe
df16 = pd.read_csv('data_2016.csv',index_col=0)
df16.insert(9,"EMPLOYER_ADDRESS_2",np.nan)
df16.insert(28,"PW_WAGE_LEVEL",np.nan)
# df16.fillna(0)

#Homogenisation of columns names
df14.columns = columns_names
df16.columns = columns_names

result = df14.merge(df15,how='outer',on=columns_names)
result = result.set_index('CASE_NUMBER')
result = result.reset_index(inplace=True).drop_duplicates(subset='CASE_NUMBER', keep='last')

final_result = result.merge(df16, how='outer',on=columns_names)
final_result = final_result.set_index('CASE_NUMBER')
final_result = final_result.reset_index(inplace=True).drop_duplicates(subset='CASE_NUMBER', keep='last')

final_result.reset_index(inplace=True)
final_result.to_excel('merged_data_bis.xlsx')


#2014 : 519503
#2015 : 618803
#2016 : 647851
