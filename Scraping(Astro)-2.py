#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests 
from requests import exceptions
from bs4 import BeautifulSoup 
import pandas as pd


# In[2]:


df = pd.read_excel('/Users/apple/Desktop/Astro.xlsx')
#df


# In[3]:


def get_soup(url): 
    try: 
        req = requests.get(url)
        soup = BeautifulSoup(req.text)
        return soup
    except: 
        pass


# In[4]:


df_soup = df['Identifier'].apply(lambda x: get_soup(x))
#df_soup


# In[5]:


def get_specs(soup):
    try:
        specs = soup.find('div',{'class','product attribute description'}).text.strip('\n').strip().split('\r\n')
        specs.remove(specs[0])
        dic = {}
        for i in specs:
            spec_list = i.split(':')
            dicts = {spec_list[0]:spec_list[1]}
            dic.update(dicts)  
        #print(dic)
        return dic
    except:
        pass


# In[6]:


df1 = pd.Series()
df2 = pd.Series()
for s in df_soup: 
    df1 = pd.Series(get_specs(s))
    df2 = df2.append(df1)
df2    


# In[7]:


df2 = pd.DataFrame(df2)


# In[8]:


df2 = df2.transpose()
df2


# In[9]:


def get_breakdown_pdf(soup):
    try:
        breakdown_pdf = soup.find('div',{'id':'product.info.breakdown'}).find('div').find('a').get('href')
        return breakdown_pdf
    except: 
        pass


# In[10]:


df['Breakdown info'] = df_soup.apply(lambda x: get_breakdown_pdf(x))


# In[11]:


def get_info_sheet_pdf(soup):
    try:
        info_sheet_pdf = soup.find('div',{'id':'product.info.sheet'}).find('div').find('a').get('href')
        return info_sheet_pdf
    except: 
        pass


# In[12]:


df['Info Sheet'] = df_soup.apply(lambda x: get_info_sheet_pdf(x))


# In[13]:


def get_info_flyer(soup):
    try:
        info_flyer = soup.find('div',{'id':'product.info.flyer'}).find('div').find('a').get('href')
        return info_flyer
    except: 
        pass


# In[14]:


df['Info Flyer'] = df_soup.apply(lambda x: get_info_flyer(x))


# In[15]:


def get_img(soup):
    try:
        img = soup.find('div',{'class': 'product media'}).find('img').get('src')
        return img
    except: 
        pass


# In[16]:


df['Image2'] = df_soup.apply(lambda x: get_img(x))
df


# In[17]:


df2.to_excel('/Users/apple/Desktop/Specifications.xlsx')


# In[18]:


df.to_excel('/Users/apple/Desktop/Astro_Scraped.xlsx')


# In[19]:


df_merged = pd.concat([df,df2],axis = 1)


# In[20]:


df_merged.to_excel('/Users/apple/Desktop/Astro_last_version.xlsx')

