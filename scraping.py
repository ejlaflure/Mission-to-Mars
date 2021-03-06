# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {"executable_path" : "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    hem_title_1, hem_img_url_1, hem_title_2, hem_img_url_2, hem_title_3, hem_img_url_3, hem_title_4, hem_img_url_4 = hemisphere_info(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title, 
        "news_paragraph": news_paragraph, 
        "featured_image": featured_image(browser), 
        "facts": mars_facts(), 
        "hem_title_1": hem_title_1, 
        "hem_img_url_1": hem_img_url_1,
        "hem_title_2": hem_title_2, 
        "hem_img_url_2": hem_img_url_2,
        "hem_title_3": hem_title_3, 
        "hem_img_url_3": hem_img_url_3,
        "hem_title_4": hem_title_4, 
        "hem_img_url_4": hem_img_url_4,
        "last_modified": dt.datetime.now()
        }
    
    # Closing browser
    browser.quit()

    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        # Begin Scrapping
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except AttributeError:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    # Converting the DataFrame back to HTML
    return df.to_html()

def hemisphere_info(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Create empty DataFrame
    hemisphere_info = pd.DataFrame(columns=["title", "image_url"])

    hemispheres = img_soup.find_all("div", class_="description")
    # Loop through all 4 hemispheres and collect the titles and images
    for div in hemispheres:
        title = div.find("a").find("h3").text
        href = div.find("a")["href"]
        link = f'https://astrogeology.usgs.gov{href}'
        browser.visit(link)
        try:
            img_url = browser.links.find_by_partial_text("Sample")["href"]
        except AttributeError:
            return None
        hemisphere_info = hemisphere_info.append({'title' : title, 'image_url' : img_url}, ignore_index=True)

    # Identify the titles and images specifically
    hem_title_1 = hemisphere_info['title'][0]
    hem_img_url_1 = hemisphere_info['image_url'][0]
    hem_title_2 = hemisphere_info['title'][1]
    hem_img_url_2 = hemisphere_info['image_url'][1]
    hem_title_3 = hemisphere_info['title'][2]
    hem_img_url_3 = hemisphere_info['image_url'][2]
    hem_title_4 = hemisphere_info['title'][3]
    hem_img_url_4 = hemisphere_info['image_url'][3]

    return hem_title_1, hem_img_url_1, hem_title_2, hem_img_url_2, hem_title_3, hem_img_url_3, hem_title_4, hem_img_url_4

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())