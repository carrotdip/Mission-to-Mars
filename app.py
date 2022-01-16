#Import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Set up Flask Routes, one for main HTML page and one to scrape new data
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)
if __name__ == "__main__":
   app.run()

# #Reuse scraping.py code to insert into a function
# def mars_news(browser):

#    # Visit the mars nasa news site
#    url = 'https://redplanetscience.com/'
#    browser.visit(url)

#    # Optional delay for loading the page
#    browser.is_element_present_by_css('div.list_text', wait_time=1)

#    # Convert the browser html to a soup object and then quit the browser
#    html = browser.html
#    news_soup = soup(html, 'html.parser')

#    # Add try/except for error handling
#    try:
#        slide_elem = news_soup.select_one('div.list_text')
#        # Use the parent element to find the first 'a' tag and save it as 'news_title'
#        news_title = slide_elem.find('div', class_='content_title').get_text()
#        # Use the parent element to find the paragraph text
#        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
#    except AttributeError:
#         return None, None

#    return news_title, news_p

# #Reuse scraping.py code to insert image scraping into function
# def featured_image(browser):
#     # Visit URL
#     url = 'https://spaceimages-mars.com'
#     browser.visit(url)

#     # Find and click the full image button
#     full_image_elem = browser.find_by_tag('button')[1]
#     full_image_elem.click()

#     # Parse the resulting html with soup
#     html = browser.html
#     img_soup = soup(html, 'html.parser')

#     # Add try/except for error handling
#     try:
#         # Find the relative image url
#         img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

#     except AttributeError:
#         return None

#     # Use the base url to create an absolute url
#     img_url = f'https://spaceimages-mars.com/{img_url_rel}'

#     return img_url

# #Refactor mars facts
# def mars_facts():
#     # Add try/except for error handling
#     try:
#         # Use 'read_html' to scrape the facts table into a dataframe
#         df = pd.read_html('https://galaxyfacts-mars.com')[0]

#     except BaseException:
#         return None

#     # Assign columns and set index of dataframe
#     df.columns=['Description', 'Mars', 'Earth']
#     df.set_index('Description', inplace=True)

#     # Convert dataframe into HTML format, add bootstrap
#     return df.to_html()

# # Refactor hemisphere data scraping
# def hemisphere_images(browser):
# # 1. Use browser to visit the URL
#     url = 'https://marshemispheres.com/'
#     browser.visit(url)

#     # 2. Create a list to hold the images and titles.
#     hemisphere_image_urls = []

#     # 3. Write code to retrieve the image urls and titles for each hemisphere.
#     links = browser.find_by_css('.results .item>a.product-item img')
#     for i in range(len(links)):
#         hemispheres = {}
#         try:
#             browser.find_by_css('.results .item > a.product-item img')[i].click()
#         except:
#             pass
#         elem = browser.links.find_by_text('Sample')
#         img_url = elem['href']
#         hemispheres['img_url'] = img_url
#         title = browser.find_by_css('h2.title').text
#         hemispheres['title'] = title
#         hemisphere_image_urls.append(hemispheres)
#         browser.back()

#     # 4. Print the list that holds the dictionary of each image url and title.
#     return hemisphere_image_urls