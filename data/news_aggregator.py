import requests
from bs4 import BeautifulSoup

def get_news(stock):
    """
    Fetches latest news headlines for a given stock using Google News.
    Returns a list of top 5 headlines.
    """
    url = f"https://news.google.com/search?q={stock}%20stock"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    headlines = soup.find_all('a', class_='DY5T1d')
    return [h.text for h in headlines[:5]]

def get_news_for_stocks(stocks):
    """
    Fetches news headlines for a list of stocks.
    Returns a dict: {stock: [headlines]}
    """
    news_dict = {}
    for stock in stocks:
        news_dict[stock] = get_news(stock)
    return news_dict
