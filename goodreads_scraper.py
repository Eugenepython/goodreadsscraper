from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    book_url = request.form['book_url']
    output_file = "reviews.txt"

    get_book_reviews(book_url, output_file)

    with open(output_file, 'r', encoding='utf-8') as file:
        reviews = file.read()

    return render_template('index.html', reviews=reviews)

def get_book_reviews(book_url, output_file):
    headers = {
        'User-Agent': 'Your User Agent',  # Set a proper user agent
    }

    response = requests.get(book_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        review_cards = soup.find_all('article', class_='ReviewCard')

        if review_cards:
            with open(output_file, 'w', encoding='utf-8') as file:
                review_counter = 0

                for review_card in review_cards:
                    formatted_span = review_card.find('span', class_="Formatted")

                    if formatted_span:
                        file.write(formatted_span.text.strip() + '\n')
                        review_counter += 1

                        if review_counter == 12:
                            break

                time.sleep(2)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == "__main__":
    app.run(debug=True)
