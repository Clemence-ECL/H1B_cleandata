from bs4 import BeautifulSoup
import os
import os.path
import sys
import dryscrape


def get_soc_name(soc_code):
  url = 'http://www.oesc.state.ok.us/OWN/4002022900/'+soc_code+'.htm'
  sess = dryscrape.Session(base_url=url)
  sess.visit(url)
  html = sess.body()
  soup = BeautifulSoup(html, 'lxml')
  try :
    soc_name = soup.find_all('th')
    for name in soc_name :
      if soc_code in name.text :
        soc_name_final = name.text
        break
    return soc_name_final.split('(')[0].strip()
  except UnboundLocalError:
    try :
      url = 'https://www.onetonline.org/find/quick?s='+soc_code
      sess = dryscrape.Session(base_url=url)
      sess.visit(url)
      html = sess.body()
      soup = BeautifulSoup(html, 'lxml')

      if soup.find('td',class_='report2ed')!=None :
        soc_name = soup.find('td',class_='report2ed').a.text
        if '(' in soc_name :
          soc_name=soc_name.split('(')[1].replace(')','')
        print(soc_name)
        return soc_name
      if soup.find('div',id='realcontent')==None :
        # print('No internet match')
        return str()
      if 'Closest matches are shown first.'in soup.find('div',id='realcontent').text:
        # print('No internet match')
        return str()
    except UnboundLocalError:
      # print('Not referenced soc name')
      return str()


# print(get_soc_name('15-1051'))
