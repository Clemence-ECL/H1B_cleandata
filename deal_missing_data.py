import pandas as pd
import numpy as np
import pickle
from fill_soc_name import get_soc_name
import string
import math

# df = pd.read_excel('merged_data_bis.xlsx',index_col=0)
# df.to_pickle('merged_data_bis.pkl')
name_file = 'merged_data_20000'
df = pd.read_excel(name_file+'.xlsx')

# df = pd.read_pickle('merged_data_bis.pkl')
df.reset_index(inplace=True)
df.fillna(0)
columns = list(df.columns.values)

#Count the NaN values
print(df.isnull().sum())

#Drop unecessary columns
del df['VISA_CLASS'] #always H1-B
del df['EMPLOYER_ADDRESS2'] # too few data, not relevant
del df['EMPLOYER_POSTAL_CODE']
del df['EMPLOYER_PROVINCE'] # mostly the same than the state
del df['EMPLOYER_PHONE_EXT']
del df['AGENT_ATTORNEY_NAME']
del df['AGENT_ATTORNEY_CITY']
del df['AGENT_ATTORNEY_STATE']
del df['WILLFUL VIOLATOR'] #few values and always N when there are some
del df['WORKSITE_COUNTY']
del df['WORKSITE_POSTAL_CODE']
del df['ORIGINAL_CERT_DATE'] #too few values
del df['FULL_TIME_POSITION']
del df['PW_WAGE_SOURCE']
del df['PW_WAGE_SOURCE_YEAR']
del df['PW_WAGE_SOURCE_OTHER']
del df['H-1B_DEPENDENT']
del df['EMPLOYER_PHONE']

#Delete rows with too few data
df = df.dropna(thresh=7)
df.reset_index(inplace=True)


# Fill the missing values with other lines
def fill_data_one_el(df,full_data,empty_data,missing_el_pos):
  #they are both columns that run together such as soc_code/soc_name
  #we suppose it works for one missing element

  #find the corresponing value in full_data
  corresponding_data = df.loc[missing_el_pos,full_data]
  if pd.isnull(corresponding_data) :
    return
  #look for a similar value in full_data where empty_data is not empty
  m,n = df.shape
  for i in range(m-1):
    if df.loc[i,full_data]==corresponding_data and i != missing_el_pos:
      if not pd.isnull(df.loc[i,empty_data]):
        searched_value = df.loc[i,empty_data]
        break
  #reassign value
  try :
    df.loc[missing_el_pos,empty_data]=searched_value
  except UnboundLocalError:
    pass



m,n=df.shape
for i in range(m-1):
#Filling soc name
  if pd.isnull(df.loc[i,'SOC_NAME']):
    if df.loc[i,'SOC_CODE']=='15-1031':
      df.loc[i,'SOC_NAME']='Software Developers, Applications'
    elif df.loc[i,'SOC_CODE']=='15-1051':
      df.loc[i,'SOC_NAME']='Computer Systems Analysts'
    elif df.loc[i,'SOC_CODE']=='15-1021':
      df.loc[i,'SOC_NAME']='Computer Programmers'
    else :
      try :
        internet_value = get_soc_name(df.loc[i,'SOC_CODE'])
      except TypeError:
        internet_value=str()
      if internet_value!=str():
        df.loc[i,'SOC_NAME']=internet_value
      else :
        fill_data_one_el(df,'SOC_CODE','SOC_NAME',i)

#Filling employer state
  if pd.isnull(df.loc[i,'EMPLOYER_STATE']):
    fill_data_one_el(df,'EMPLOYER_CITY','EMPLOYER_STATE',i)
#Filling country
  if pd.isnull(df.loc[i,'EMPLOYER_COUNTRY']):
    fill_data_one_el(df,'EMPLOYER_STATE','EMPLOYER_COUNTRY',i)

# Filling pay wage level
  if pd.isnull(df.loc[i,'PW_WAGE_LEVEL']):
    fill_data_one_el(df,'SOC_CODE','PW_WAGE_LEVEL',i)
# Filling worksite state
  if pd.isnull(df.loc[i,'WORKSITE_STATE']):
    fill_data_one_el(df,'WORKSITE_CITY','WORKSITE_STATE',i)


#Deal with the wage rate of pay (from/to)
  if isinstance(df.loc[i,'WAGE_RATE_OF_PAY'],str):
    if '-' in df.loc[i,'WAGE_RATE_OF_PAY']:
      data1 = df.loc[i,'WAGE_RATE_OF_PAY'].split('-')[0]
      data2 = df.loc[i,'WAGE_RATE_OF_PAY'].split('-')[1]
      if data1!='':
        df.loc[i,'WAGE_RATE_OF_PAY']=float(data1)
      if data2!='':
        df.loc[i,'WAGE_RATE_OF_PAY_TO']=float(data2)

#Getting rid of unit of pay
  if df.loc[i,'WAGE_UNIT_OF_PAY']=='Hour':
    df.loc[i,'WAGE_RATE_OF_PAY']=df.loc[i,'WAGE_RATE_OF_PAY']*2080
    df.loc[i,'WAGE_RATE_OF_PAY_TO']=df.loc[i,'WAGE_RATE_OF_PAY_TO']*2080

  if df.loc[i,'PW_UNIT_OF_PAY']=='Hour':
    df.loc[i,'PREVAILING_WAGE']=df.loc[i,'PREVAILING_WAGE']*2080

#Getting rid of wage rate from and wage rate to
  if not pd.isnull(df.loc[i,'WAGE_RATE_OF_PAY_TO']):
    df.loc[i,'WAGE_RATE_OF_PAY']=(df.loc[i,'WAGE_RATE_OF_PAY']+df.loc[i,'WAGE_RATE_OF_PAY_TO'])/2



del df['PW_UNIT_OF_PAY']
del df['WAGE_UNIT_OF_PAY']
del df['WAGE_RATE_OF_PAY_TO']



df.to_excel(name_file+'bis.xlsx',index=False)


print(df.isnull().sum())
