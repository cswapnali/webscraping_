import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

customer_name = []
customer_review = []

pages = np.arange(1,16)

for page in pages:
    url = 'https://www.flipkart.com/saf-painting-ink-20-inch-x-14/product-reviews/itme0cd5de2f576b?pid=PTGEQVXAU5Z5JCEF&lid=LSTPTGEQVXAU5Z5JCEFVHQUT4&marketplace=FLIPKART&page=' + str(page)
    page = requests.get(url)
    htmlContent = page.content
    #print(htmlContent)
    soup = BeautifulSoup(htmlContent, 'html.parser')
    #print(soup.prettify)
    
    data_str = ''
    for item in soup.find_all('p', class_ = '_2sc7ZR _2V5EHH'):
        data_str = data_str + item.get_text()
        customer_name.append(data_str)
        data_str = ''
    
    data_str = ''
    for item in soup.find_all('p', class_ = '_2-N8zT'):
        data_str = data_str + item.get_text()
        customer_review.append(data_str)
        data_str = ''

data = {'NAMES' : customer_name, 'REVIEWS' : customer_review}
df = pd.DataFrame(data)
df.to_csv('Flipkart_prod_review.csv')
