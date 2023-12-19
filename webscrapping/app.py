from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    result_df = scrape_flipkart_reviews(url)
    return render_template('result.html', result=result_df.to_html())

def scrape_flipkart_reviews(url):
    page = requests.get(url)
    html_content = page.content
    soup = BeautifulSoup(html_content, 'html.parser')

    data_list = []

    pages_text = soup.find('div', class_='_2MImiq _1Qnn1K').find('span').text
    total_pages = int(pages_text.split()[-1])

    for page_num in range(1, total_pages + 1):
        page_url = f"{url}&page={page_num}"
        page = requests.get(page_url)
        html_content = page.content
        soup = BeautifulSoup(html_content, 'html.parser')

        reviews = soup.find_all('div', class_='_1AtVbE col-12-12')
        for review in reviews:
            try:
                customer_name = review.find('p', class_='_2sc7ZR _2V5EHH').text.strip()
                rating_star = review.find('div', class_='_3LWZlK _1BLPMq').text.strip()
                review_text = review.find('p', class_='_2-N8zT').text.strip()

                data_list.append({
                    'Customer Name': customer_name,
                    'Rating Star': rating_star,
                    'Review': review_text
                })
            except:
                pass

    result_df = pd.DataFrame(data_list)
    return result_df

if __name__ == '__main__':
    app.run(debug=True)
