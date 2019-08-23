#HEMISPHERES
# Get the image path for the article
def scrape():
    browser = init_browser()

    # Visit https://mars.nasa.gov/news
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    
    #step through the pages to get to the page with the image
    time.sleep(1)
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #scrap the page, gathering the image title and url
    title = soup.select_one("div.content h2.title").get_text()
    img_url = soup.select_one("div.downloads ul li a").get("href")
    
    # Store data in a dictionary
    hemisphere = {
        "title": title,
        "url": img_url
    }
    
    # Close the browser after scraping
    browser.quit()
    
    return hemisphere
    
scrape()