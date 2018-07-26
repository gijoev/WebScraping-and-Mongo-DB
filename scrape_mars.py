import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
import requests
import os
import splinter

def scrape():

    browser = Browser("chrome", executable_path = r"C:\Users\nisha\OneDrive\DATASCIENCE\Week13MongoDBBeautifulSoup\Homework\Web-Scraping-and-Mongo-DB\chromedriver.exe", headless=False)
    result = {}
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup = bs(html, 'html.parser')
    #Test by checking if Title shows up
    #soup.title.text
    print("Getting news title")
    result["news_title"] = soup.find('div', class_="content_title").text
    result["news_para"] = soup.find('div', class_="article_teaser_body").text
    #print(result["news_title"])
    print("Got news title and paragraph")
    

    #SECOND TEST. It works in my test
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA16883-1920x1200.jpg"
    browser.visit(featured_image_url)
    time.sleep(5)
    result["featured_image"] = featured_image_url
    print("Got featured image")
    
    #TWITTER - Worked in test
    twitter_url = "https://twitter.com/marswxreport?lang=en "
    browser.visit(twitter_url)
    time.sleep(5)
    twitter_response = requests.get(twitter_url)
    soup_weather = bs(twitter_response.text, 'html.parser')
    result["mars_weather"] = soup_weather.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print("Got twitter information")
    

    #Mars Facts
    print('start of Facts')
    url="https://space-facts.com/mars/"
    marsFacts=pd.read_html(url)
    facts=marsFacts[0]
    facts.columns= ['fact', 'Number']
    facts=facts.set_index('fact')['Number'].to_dict()
    result['facts']=facts
    print('end of Facts')
    
    #Mars hemispheres that works
    print('start of hemisphere images')
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/'
    browser.visit(mars_hemisphere_url)
    time.sleep(5)
    html=browser.html
    soup = bs(html, 'html.parser')
    soup.title.text
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

    #Creating a dictionary. The key is the title and the value is the URL.
    mars_hemispheres_images = [
        {'title': title_list[0], 'img_url': url_list[0]},
        {'title': title_list[1], 'img_url': url_list[1]},
        {'title': title_list[2], 'img_url': url_list[2]},
        {'title': title_list[3], 'img_url': url_list[3]}
    ]

    result["mars_hemispheres_images"] = mars_hemispheres_images
    print('end of hemisphere images')
    
    return result
    
    
                       
    
    

    
    