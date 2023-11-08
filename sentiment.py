# See https://shashank-vemuri.medium.com/ for the original code and inspiration of this project.

import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.request import urlopen
from urllib.request import Request

# Needed for first run.
# import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time

# Globals
finviz_url = 'https://finviz.com/quote.ashx?t='

def getTickerNewsTablesList(tickers):
    try:
        news_tables = {}

        for x in tickers:
            url = finviz_url + x
            request = Request(url=url,headers={'user-agent': 'stock_screener'}) 
            response = urlopen(request)

            # Use beautiful soup to get html form webpage
            html = BeautifulSoup(response, features="lxml")

            # Get news table from each ticker site and store in list
            news_table = html.find(id='news-table')
            news_tables[x] = news_table

            time.sleep(0.1)   

    except KeyError:
        pass

    return news_tables

def getRecentHeadlinesList(news_tables, tickers):
    try:
        headline_count = 3
        headlines = {}

        for x in tickers:
            # Get all the rows from the table
            row_list = news_tables[x].findAll('tr')
            ticker_headlines = []
        
            for i, row in enumerate(row_list):

                # Get headline
                headline = row.a.text
                # Get date and time information
                date_and_time = (row.td.text).strip()
                # Get headline company
                company = row.span.text

                ticker_headlines.append([headline, date_and_time, company])
                if i == headline_count-1:
                    break

            headlines[x] = ticker_headlines

    except KeyError:
        pass

    return headlines

def sentimentAnalysis(headlines):

    data_list = [
        {'Ticker': ticker, 'Headline': item[0], 'Date': item[1], 'Website': item[2]}
        for ticker, ticker_data in headlines.items()
        for item in ticker_data
    ]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)

    # Use NLTK sentiment analyzer to generate neg, neutral, pos and compound polarity scores
    analyzer = SentimentIntensityAnalyzer()
    scores = df['Headline'].apply(analyzer.polarity_scores).tolist()
    df = df.join(pd.DataFrame(scores), rsuffix='_right')

    # Calculate the mean compound value for each ticker
    mean_compound = df.groupby('Ticker')['compound'].mean().reset_index()
    mean_compound.rename(columns={'compound': 'Sentiment'}, inplace=True)

    return df, mean_compound

def sentiment(tickers):
    news_tables = getTickerNewsTablesList(tickers)
    headlines = getRecentHeadlinesList(news_tables, tickers)
    raw, sentiment = sentimentAnalysis(headlines)
    
    print(raw)
    print('\n')
    print(sentiment)

    return raw, sentiment