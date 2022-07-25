#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import requests
import bs4 as bs
import pandas as pd
import time

# Write a single function to:
# 1. Get the list of topics from the topics page
# 2. Get list of top repos from the individual topic pages
# 3. For each topic create a csv of the top repos for the topic 

# In[12]:


def get_topic_title(doc):
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tag = doc.find_all('p',{'class': selection_class })
    
    topic_title = []
    for tag in topic_title_tag:
        topic_title.append(tag.text)
    return topic_title

def get_topic_desc(doc):
    desc_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tag = doc.find_all('p',{'class':desc_selector})
    topic_desc = []
    for desc in topic_desc_tag:
        topic_desc.append(desc.text.strip())
    return topic_desc
    
    
def get_topic_url(doc):
    base_url = "https://github.com"
    url_selector = 'no-underline flex-1 d-flex flex-column'
    topic_link_tag = doc.find_all('a',{'class':url_selector})        
    topic_urls = []
    
    for url in  topic_link_tag:
        topic_urls.append(base_url+url['href'])
    return topic_urls
        
def scrape_topics(num):
    topic_url = 'https://github.com/topics?page={}'.format(num)
    response = requests.get(topic_url)
    if response.status_code !=200:
        print("Process Stops restarting..........")
        time.sleep(20)
        os.system("ScraperCode.py 1")
#         raise Exception('Failed to load the page {}'.format(topic_url))
        
    doc = bs.BeautifulSoup(response.text,'html.parser')
    topics_dict = {
        'title' : get_topic_title(doc),
        'description' : get_topic_desc(doc),
        'url' : get_topic_url(doc),
        
    }
#     print(topics_dict)
    return pd.DataFrame(topics_dict)


# In[3]:


def get_topic_page(topic_url):
    response = requests.get(topic_url)
    if response.status_code !=200:
        print("Process Stops restarting..........")
        time.sleep(20)
        os.system("ScraperCode.py 1")
        # raise Exception('Failed to load the page {}'.format(topic_url))
    topic_doc = bs.BeautifulSoup(response.text,'html.parser')
    return topic_doc

def get_repo_info(h3_tag, star_tags):
    #gives all info about repository
    base_url = "https://github.com"
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = repo_url = base_url + a_tags[1]['href']
    star_count = parse_star_count(star_tags.text)
    return username, repo_name, star_count, repo_url

def parse_star_count(stars_count):
    stars_str = stars_count.strip()
    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1])*1000)
    return (int(stars_str))
        

def get_topic_repos(topic_doc):
    
#     get h3 tag for repo name, url, etc.
    h3_selection_class = 'f3 color-fg-muted text-normal lh-condensed'
    repo_tags = topic_doc.find_all('h3',{'class': h3_selection_class})
    
#     get star tags
    star_selector = 'Counter js-social-count'
    star_tags = topic_doc.find_all('span',{'class': star_selector})
    
#     get repo info
    topic_repos_dict = {
        'username':[],
        'repo_name':[],
        'stars': [],
        'repo_url':[]
    }
    for i in range (len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i],star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[2])
        topic_repos_dict['repo_url'].append(repo_info[3])
        
#     put all in dataframe
    topic_repos = pd.DataFrame(topic_repos_dict)
    return topic_repos

def scrape_topic(topic_url,path):

    if os.path.exists(path):
        print("File {} already exits.".format(path))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path,index=None)
    


# In[4]:


def scrape_topics_repos():
    for i in range(1,7):
        topics_df = scrape_topics(i)

        os.makedirs('Resultant Data Files',exist_ok = True)

        for index,row in topics_df.iterrows():
            print("Scrapping topic {}.".format(row['title']))
            scrape_topic(row['url'],'Resultant Data Files/{}.csv'.format(row['title']))
        


# In[18]:

if __name__ == '__main__':
    scrape_topics_repos()


# ###### Helper site

# https://jovian.ai/aakashns-6l3/scraping-github-topics-repositories

# In[ ]:




