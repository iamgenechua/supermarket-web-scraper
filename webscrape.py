from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from selenium import webdriver

# initialise my product set
product_set = set()

# name the output file to write to local disk
out_filename = "redmart_products.csv"

# header of csv file to be written
headers = "product_name,price,weight \n"

# opens file, and writes headers
f = open(out_filename, "a")
f.write(headers)

for i in range(9):
    # URl to web scrape from.
    page_url = "https://redmart.lazada.sg/meat-and-seafood/?m=redmart&page=" + str(i+1)

    # access chrome webdriver 
    driver = webdriver.Chrome()

    # access the url page with the Chrome webdriver
    driver.get(page_url)

    # Execute JS on that page with "return document.documentElement.outerHTML" to load dynamic elements
    result = driver.execute_script("return document.documentElement.outerHTML")

    # quit the driver once done
    driver.quit()

    # parse the resulting html after loading all dynamic elements
    page_soup = soup(result, 'lxml')

    # Product containers are found in <div class="RedmartProductCard-content"></div>
    # Finds each product from the store page
    containers = page_soup.findAll("div", {"class" : "RedmartProductCard-content"})

    # loops over each product and grabs attributes about each product
    for container in containers:
        
        # Grabs h4 tag enclosing the product name and grabs product name with .text
        product_name = container.find("h4", {"class" : "RedmartProductCard-title"}).text

        if product_name not in product_set:
            product_set.add(product_name)

            # Grabs the div enclosing product price and grabs text with .text
            price = container.find("div", {"class" : "RedmartProductCard-price"}).text

            # Grabs the div enclosing the product weight and grabs text with .text
            weight = container.find("div", {"class" : "RedmartProductCard-weight"}).text

            # Write product, price & weight to csv file
            f.write(product_name + ", " + price + ", " + weight + "\n")


# close the file
f.close()



