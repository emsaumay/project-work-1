from flask import Flask, render_template
import requests as r
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/demo')
def demo():
    return render_template('demo.html', news=get_news())

def sentiment(input):
    res = r.get(f"https://text.saumay.workers.dev/?text={input}").json()
    return res

def get_news():
    url = "https://www.moneycontrol.com/news/business/stocks/"
    news = []
    for i in range(1, 2):
        response = r.get(f"{url}page-{i}/")
        soup = BeautifulSoup(response.text, 'html.parser')

        list_items = soup.find_all('li', class_='clearfix')

        for item in list_items:
            a_tag = item.find('a')

            if a_tag and 'title' in a_tag.attrs:
                title_value = a_tag['title']
                news.append(title_value)
                print(title_value)
                i+=1
    return news

def analysis():
    news = get_news()
    positive = []
    negative = []
    for d in news:
        res = sentiment(d)
        plus = res['response'][1]['score']
        minus = res['response'][0]['score']
        positive.append(d) if int(plus*100) > int(minus*100) else negative.append(d)
    return positive, negative

if __name__ == '__main__':
    app.run()