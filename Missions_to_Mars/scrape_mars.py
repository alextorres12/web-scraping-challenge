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

    



