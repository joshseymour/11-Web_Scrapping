from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #Note: had to remove executable path due to issue with the way chromedriver is loaded.  
    #It creates 2 versions of the app, which causes conflict when running.  If running on local PC, uncomment executable_path
    # and add **executable_path between "chrome" and headless
    return Browser("chrome", headless=False)

#Mars News Data
#Scrape the first news article https://mars.nasa.gov/news and get the first result
def scrape():
    browser = init_browser()

    # Visit https://mars.nasa.gov/news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    #give the page time to load
    time.sleep(1)

    # Get the first new titles
    list_title= soup.select_one("ul.item_list li.slide")
    title = list_title.find("div", class_="content_title").get_text()
 
    # Get the first articles teaser body content
    content = list_title.find("div", class_="article_teaser_body").get_text()

    # Store data in a dictionary
    mars_news = {
        "news_title": title,
        "mars_p": content
    }

    # Close the browser after scraping
    browser.quit()

    #JPL Mars Space Images
    # Get the image path for the article
    browser = init_browser()

    # Visit https://mars.nasa.gov/news
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    img_url = "https://www.jpl.nasa.gov"
    browser.visit(url)

    #give the page time to load
    time.sleep(1)
    
    #step through the pages to get to the page with the image
    browser.click_link_by_partial_text('FULL IMAGE')
    
    #give the page time to load
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the first new titles
    image = soup.select_one("figure.lede a img").get("src")
    
    featured_img_url = img_url + image
    
    browser.quit()

    #Mars Weather
    #Scrape the latest tweet about Mars weather
    browser = init_browser()

    # Visit https://mars.nasa.gov/news
    url = "https://twitter.com/marswxreport?lang-en"
    browser.visit(url)

    #give the page time to load
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the first new titles
    mars_weather = soup.select_one("div.js-tweet-text-container p").get_text()

    # Close the browser after scraping
    browser.quit()

    # Mars Facts
    #give pandas the URL
    url = 'https://space-facts.com/mars'
    tables = pd.read_html(url)[1]
    tables.columns = ['Description', 'Value']
    space_facts = tables.iloc[1:]
    space_facts.set_index('Description', inplace=True)

    #HEMISPHERES
    # Get the image path for the article
    browser = init_browser()

    #create list of links to click through with browser.click_link_by_partial_text
    sites = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']
    
    hemisphere_image_url = []
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    
    for site in sites:
        try:
            # Visit https://mars.nasa.gov/news    
            browser.click_link_by_partial_text(site)
            time.sleep(1)

            # Scrape page into Soup
            html = browser.html
            soup = bs(html, "html.parser")

            #scrap the page, gathering the image title and url
            title = soup.find("h2", class_="title").get_text()
            img_url = soup.find("a", text="Sample").get("href")

            # Store data in a dictionary
            hemisphere = {
                "title": title,
                "img_url": img_url
                }
            hemisphere_image_url.append(hemisphere)
            
        except:
            hemisphere_image_url.append({
                "title": None,
                "img_url": None
                }) 
        
        browser.back()
    
    # Close the browser after scraping
    browser.quit()

    mars_data = {
    "news": mars_news, 
    "image": featured_img_url,
    "weather": mars_weather,
    "facts": space_facts,
    "hemisphere": hemisphere_image_url    
    }
      
    return mars_data