
# coding: utf-8

# <h3>Setup</h3>
# 
# Use splinter to navigate the sites when needed and BeautifulSoup to help find and parse out the necessary data.

# In[2]:


# Dependencies
import os
from bs4 import BeautifulSoup as bs
#from bs4 import BeautifulSoup
import requests
import splinter
from splinter import Browser
#browser = Browser("chrome", headless = False)
browser = Browser("chrome", headless=False)


# In[2]:


get_ipython().system('where chromedriver')


# In[19]:


##Response Method.
url = "https://mars.nasa.gov/news/"
# Retrieve page with the requests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')
# Examine the results, then determine element that contains sought info
#print(soup.prettify())


# In[28]:


##Browser Method.
## NASA Mars News## NASA 
#URL of page to be scraped
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

html=browser.html
soup = bs(html, 'html.parser')
#Test by checking if Title shows up
soup.title.text


# <h2>NASA Mars News</h2><hr>
# <blockquote><strong>Website to Scrape:</strong> https://mars.nasa.gov/news/</blockquote>
# <p>Instructions: Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. 
# Assign the text to variables that you can reference later.</p>
# <p>Please note that I have demonstrated a few ways to get the latest News Title and Paragraph.</p>

# Approach 1

# In[36]:


# Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. 
##Approach 1. 
title = soup.find('div', class_="content_title").text
print(title)
para = soup.find('div', class_="article_teaser_body").text
print(para)
# news_p = soup.find("div", class_="article_teaser_body")  <-MY ORIGINAL
# print(news_p)


# Approach 2

# In[35]:


#Approach 2.
news_title = soup.find('div', class_ = "content_title").text
print(news_title)
#news_p = soup.find("div", class_ = "article_teaser_body")
news_p = soup.find('div', class_="rollover_description_inner").text
print(news_p)


# Approach 3

# In[37]:


#Approach 3.
#Iterate through homepage and all articles to find title and paragraph objects
#news_title = "Vice President Pence Visits JPL, Previews NASA’s Next Mars Mission Launch"
#news_p = "A week before NASA launches its next mission to Mars, Vice President Mike Pence toured on Saturday, April 28, the birthplace of numerous past, present and future space missions at the agency’s Jet Propulsion Laboratory in Pasadena, California."

#Append Lists through parsing
news_title_lists = []
url_lists = []
news_url_lists = []
news_paragraph_lists = []

#Set browser as html object
html = browser.html
#Parse HTML using Beautiful Soup
soup = bs(html, "html.parser")
sidebar = soup.find("ul", class_="item_list")
categories = sidebar.find_all("li")
#print(categories)
#print(sidebar)
#Retrieve all elements
for category in categories:
    news_url = category.find("a")["href"]
    url_lists.append(news_url)
    titles = category.find(class_="content_title")
    paragraph = category.find(class_="article_teaser_body")
    news_paragraph_lists.append(paragraph)
    for title in titles:
        headings = title.text.strip()
        news_title_lists.append(title)

#Append news_url_lists by concatenating url with news links

news_url_lists = ["https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest" + url for url in url_lists]

news_title_lists[0]

news_paragraph_lists[0]


# In[39]:


##Tested Find Alls.
# news_p1 = soup.find_all('div', class_="rollover_description_inner")
# print(news_p1)
# news_title = soup.find_all('div', class_ = "content_title")
# print(news_title)


# <h3>JPL Mars Space Images - Featured Image</h3><hr>
# <blockquote><strong>URL Used for Scraping: </strong>https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars</blockquote>

# In[43]:


# Visit the url for JPL's Featured Space Image here.

# Use splinter to navigate the site and find the image url for the current Featured Mars Image 
#and assign the url string to a variable called featured_image_url.
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
#featured_image_url_med = "https://www.jpl.nasa.gov//spaceimages/images/mediumsize/PIA16883_ip.jpg"
featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA16883-1920x1200.jpg"
# Make sure to save a complete url string for this image.Make sure to find the image url to the full size .jpg image. 
browser.visit(featured_image_url)


# In[50]:


##The featured image keeps changing everyday. 
#featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16919_hires.jpg"
# browser.visit(featured_image_url)
###############################################################################
# jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA16028_ip.jpg'
# browser.visit(featured_image_url)


# In[1]:


jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)
#navigate to link
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(20)
browser.click_link_by_partial_text('more info')
image_html = browser.html
soup = bs(image_html, "html.parser")
image_path = soup.find('figure', class_='lede').a['href']
featured_image_url = "https://www.jpl.nasa.gov/" + image_path


# <h3>Mars Weather</h3><hr>
# <blockquote><strong>Mars Weather Twitter account Link: </strong> https://twitter.com/marswxreport?lang=en <br></blockquote>
# Visit the Mars Weather twitter account listed in the URL above and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.<br>
# Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'

# In[58]:


twitter_url = "https://twitter.com/marswxreport?lang=en "
twitter_response = requests.get(twitter_url)
soup_weather = bs(twitter_response.text, 'html.parser')
mars_weather = soup_weather.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
#mars_weather = soup_weather.find("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" data-aria-label-part="0" lang="en")
print(mars_weather)


# In[51]:


# Examine the results, then determine element that contains sought info
#print(soup_weather.prettify())


# Approach 2

# In[59]:


##Browser Method generates same results. (Second Approach)
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')
mars_weather = soup.find('p', 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
mars_weather


# <h3>Mars Weather</h3>
# <blockquote><strong>Mars fact URL: </strong>https://space-facts.com/mars/</blockquote>
# Visit the Mars Facts webpage in the URL above and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# Use Pandas to convert the data to a HTML table string.

# In[97]:


import pandas as pd


# In[98]:


url = "https://space-facts.com/mars/"


# In[99]:


#We can use the read_html function in Pandas to automatically scrape any tabular data from a page.
tables = pd.read_html(url)
tables


# In[100]:


type(tables)


# In[101]:


df = tables[0]
# df.columns = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 
#               'Orbit Distance', 'Orbit Period', 'Surface Temperature', 'First Record', 
#               'Recorded By']

#df.columns = ['One', 'Two']
df.head()


# In[108]:


mars_df = df.transpose()


# In[109]:


mars_df


# In[110]:


mars_df.columns = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 
              'Orbit Distance', 'Orbit Period', 'Surface Temperature', 'First Record', 
              'Recorded By']
#df.reset_index()


# In[111]:


mars_df.head()


# In[112]:


#Cleanup of extra rows
mars_df = mars_df.iloc[1:]
mars_df.head()


# In[113]:


#Pandas also had a to_html method that we can use to generate HTML tables from DataFrames.
# get html code for DataFrame
fact_table = mars_df.to_html(index = False)
#header = False, 
fact_table


# In[116]:


#Strip unwanted newlines to clean up the table.
#fact_table.format()
fact_table.replace('\n', '')


# In[117]:


# save the table directly to a file.
mars_df.to_html('fact_table.html')


# <h3>Mars Hemispheres</h3>
# <blockquote><strong>USGS Astrogeology URL: </strong> https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars</blockquote>
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# In[74]:


import pprint


# In[64]:


usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(usgs_url)
usgs_html = browser.html
soup = bs(usgs_html, 'html.parser')
# Examine the results, then determine element that contains sought info
#print(soup.prettify())


# In[65]:


# gets class holding hemisphere picture
returns = soup.find('div', class_="collapsible results")
hemispheres = returns.find_all('a')
hemispheres


# In[66]:


cerberus_image = browser.find_by_tag('h3')[0]
schiaparelli_image =  browser.find_by_tag('h3')[1]
syrtis_image = browser.find_by_tag('h3')[2]
marineris_image = browser.find_by_tag('h3')[3]


# In[87]:


browser.find_by_css('.thumb')[0].click()
first_img = browser.find_by_text('Sample')['href']
browser.back()

browser.find_by_css('.thumb')[1].click()
second_img = browser.find_by_text('Sample')['href']
browser.back()

browser.find_by_css('.thumb')[2].click()
third_img = browser.find_by_text('Sample')['href']
browser.back()

browser.find_by_css('.thumb')[3].click()
fourth_img = browser.find_by_text('Sample')['href']

mars_hemispheres_images = [
    {'title': cerberus_image, 'img_url': first_img},
    {'title': schiaparelli_image, 'img_url': second_img},
    {'title': syrtis_image, 'img_url': third_img},
    {'title': marineris_image, 'img_url': fourth_img}
]

pprint.pprint(mars_hemispheres_images)


# Approach 2
# <hr>

# In[71]:


##Mars Hemispheres (Approach 2)
mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/'
browser.visit(mars_hemisphere_url)
html=browser.html
soup = bs(html, 'html.parser')
soup.title.text


# In[86]:


##Loop through all the descriptions in the URL. Append the Description to a description list. Append the URL to a URL list

mars_hemispheres_images = {}
title_list = []
url_list = []
descriptions = soup.find_all('div', class_='description')
for description in descriptions:
    title = description.find('h3').text
    img_url = description.a['href']
    img_url_final = "https://astrogeology.usgs.gov" + img_url
    #print(title)
    #print(img_url_final)
    title_list.append(title)
    url_list.append(img_url_final)

#Test to make sure that the title and URLs are printing. Python's range function  - indexes 0,1,2 and 3.
# for i in range(0,4):
#     print(title_list[i])
#     print(url_list[i])

#Creating a dictionary. The key is the title and the value is the URL.
mars_hemispheres_images = [
    {'title': title_list[0], 'img_url': url_list[0]},
    {'title': title_list[1], 'img_url': url_list[1]},
    {'title': title_list[2], 'img_url': url_list[2]},
    {'title': title_list[3], 'img_url': url_list[3]}
]
#Using pprint for "pretty-print" instead of a regular print to make the dictionary easier to read.
pprint.pprint(mars_hemispheres_images)


# In[ ]:


def scrape:
    #News
    mars_dict = []
    title = soup.find('div', class_="content_title").text
    para = soup.find('div', class_="article_teaser_body").text
    print(title)
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA16883-1920x1200.jpg"
    twitter_url = "https://twitter.com/marswxreport?lang=en "
twitter_response = requests.get(twitter_url)
soup_weather = bs(twitter_response.text, 'html.parser')
mars_weather = soup_weather.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #Weather
    mars_dict.append({
        'news_title': title,
        'news_paragraph': para,
        'featured_image' : featured_image_url,
        'mars_weather': mars_weather
    })
    #Images
    #Fact
    #Hemispheres

