# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

	#hemispheres = mars_hemispheres(browser)
	#hemispheres = mars_hemispheres(browser)


    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
		"hemispheres": mars_hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

	# Scrape Mars News
	# Visit the mars nasa news site
	url = 'https://redplanetscience.com/'
	browser.visit(url)

	# Optional delay for loading the page
	browser.is_element_present_by_css('div.list_text', wait_time=1)

	# Convert the browser html to a soup object and then quit the browser
	html = browser.html
	news_soup = soup(html, 'html.parser')
	
	# Add try/except for error handling
	try:

		slide_elem = news_soup.select_one('div.list_text')
		# slide_elem.find('div', class_='content_title')

		# Use the parent element to find the first <a> tag and save it as  `news_title`
		news_title = slide_elem.find('div', class_='content_title').get_text()
		# news_title

		# Use the parent element to find the paragraph text
		news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
		# news_p
		
	except AttributeError:
		return None, None

	return news_title, news_p


# ### Featured Images

def featured_image(browser):

	# Visit URL
	url = 'https://spaceimages-mars.com'
	browser.visit(url)


	# Find and click the full image button
	full_image_elem = browser.find_by_tag('button')[1]
	full_image_elem.click()


	# Parse the resulting html with soup
	html = browser.html
	img_soup = soup(html, 'html.parser')

	try:
		# Find the relative image url
		img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
		# img_url_rel
		
	except AttributeError:
		return None
		
	# Use the base URL to create an absolute URL
	img_url = f'https://spaceimages-mars.com/{img_url_rel}'
	# img_url

	return img_url
	
# ## Mars Facts
def mars_facts():

	try:
		# use 'read_html" to scrape the facts table into a dataframe
		df = pd.read_html('https://galaxyfacts-mars.com')[0]
	
	except BaseException:
		return None

	# Assign columns and set index of dataframe
	df.columns=['description', 'Mars', 'Earth']
	df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
	return df.to_html(classes="table table-striped")

# ## Mars Hemispheres
def mars_hemispheres(browser):

	# 1. Use browser to visit the URL 
	url = 'https://marshemispheres.com/'

	browser.visit(url)

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

	return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

#browser.quit()

