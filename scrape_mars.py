import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    mars_dict = {}


    #News
    news_url = 'https://mars.nasa.gov/news'
    response = requests.get(news_url)

    soup = bs(response.text, 'html.parser') 

    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='image_and_description_container')[0].text

    mars_dict['news_title'] = news_title
    mars_dict['news_body'] = news_p

    browser.quit() 

    #Featured Image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    image_url = soup.find('img', class_='headerimage fade-in')['src']
    base_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    featured_image_url = base_image_url + image_url
    
    mars_dict['featured_image'] = featured_image_url

    browser.quit() 

    #Facts Table
    facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)

    df = tables[0]
    df.columns = ['Mars', '']
    df.set_index('Mars', inplace=True)
    table_html = df.to_html('marstable.html')

    mars_dict['html'] = table_html
    
    #Hemispheres
    hem_image_urls = []

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    for x in range(4):
        usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(usgs_url)
    
        browser.links.find_by_partial_text('Hemisphere')[x].click()
    
        html = browser.html
        soup = bs(html, 'html.parser')
    
        image_url = soup.find('li').a['href']
        title = soup.find('h2', class_='title').text
        hem_image_urls.append({'Title': title[:-9], 'Image URL': image_url})
    
        browser.back

    mars_dict["Hemispheres"] = hem_image_urls

    browser.quit()  

    return mars_dict