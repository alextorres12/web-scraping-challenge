from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    scrape_data = {}

    # Setup splinter
    executable_path= {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #### NASA Mars News ####

    # Visit NASA Mars News URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Grab HTML with BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get title and associated paragraph text
    news_title = soup.find('ul', class_='item_list').\
        find('li', class_='slide').\
        find('div', class_='content_title').a.text

    news_p = soup.find('ul', class_='item_list').\
        find('li', class_='slide').\
        find('div', class_='article_teaser_body').text

    scrape_data['Mars News Title'] = news_title
    scrape_data['Mars News Text'] = news_p

    #### JPL Mars Space Images - Featured Image ####

    # Visit JPL Mars Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click first search result
    search_result = browser.find_by_css('div[id="SearchListingPageResults"] img').first
    search_result.click()

    # Make image full screen
    full_screen = browser.find_by_css('button[class="BaseButton focus:outline-none text-contrast-none -primary -icon-only xl:text-xl inline-block"]')
    full_screen.click()

    # Parse HTML
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # Grab original image URL
    featured_image_url = soup.find('div', class_='BaseLightbox__slide__img').img['src']

    scrape_data['JPL Featured Mars Image'] = featured_image_url


    #### Mars Facts ####
    # Get tables as DataFrames
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]

    #convert to HTML table
    mars_facts_html_table = df.to_html()

    scrape_data['Mars Facts Table HTML'] = mars_facts_html_table


    #### Mars Hemispheres ####
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []
    # Get list of Hemisphere links
    image_links = browser.find_by_css('a[class="itemLink product-item"] img')

    # Loop through each link
    for i in range(len(image_links)):
        hemisphere_dict = {}
        
        # Click Link
        browser.find_by_css('a[class="itemLink product-item"] img')[i].click()
        
        # Parse HTML
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        # Grab title and image link for each hemisphere
        hemisphere_dict['title'] = soup.find('h2', class_='title').text
        hemisphere_dict['img_url'] = soup.find('div', class_='downloads').ul.li.a['href']
        
        # Append hemisphere dictionary to list of hemispheres
        hemisphere_image_urls.append(hemisphere_dict)
        browser.back()

    scrape_data['Hemisphere Images'] = hemisphere_image_urls

    browser.quit()

    return scrape_data

    
















