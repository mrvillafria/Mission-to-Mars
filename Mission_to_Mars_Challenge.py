#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[3]:


# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Parse the HTML
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# Assign title and summary text to variables
slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[15]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[16]:


df.to_html()


# In[17]:


browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[4]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[5]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemi_image = soup(html, 'html.parser')


# Examine the results and look for a div withe the class 'item'
results = hemi_image.find_all('div', class_='item')

for result in results:
        # Identify and return title of listing
        titles = result.find('h3').text

        # Find and click the titles
        browser.links.find_by_partial_text(titles).click()
        
        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='wide-image').get('src')
        
        # Use the base URL to create an absolute URL
        img_url = f'https://marshemispheres.com/{img_url_rel}'

        # Navigate back to the beginning to get the next hemisphere
        browser.back()
        
        #store img_url and title in a dictionary
        hemispheres = {
            'img_url':img_url,
            'title': titles
        }
        
        #add dictionary to list
        hemisphere_image_urls.append(hemispheres)


# In[6]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[7]:


# 5. Quit the browser
browser.quit()


# In[ ]:




