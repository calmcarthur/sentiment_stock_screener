import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.request import urlopen
from urllib.request import Request
import time

# def addCriteria():
#     # To be changed via Web App or by Hand
#     checked_indices = [0, 1, 3, 4, 5, 6, 7, 9, 11, 13, 16, 17, 27, 33, 34, 37, 51, 67, 65, 66]
#     url = 'https://finviz.com/screener.ashx?v=152&ft=4&o=-marketcap&'
#     for x in checked_indices:
#         url = url + str(x) + ','
#     return url

def generateUrls():
    mainurl = 'https://finviz.com/screener.ashx?v=152&ft=4&o=-marketcap&c=0,1,3,4,5,6,7,9,11,13,16,17,27,33,34,37,51,67,65,66'

    url_list = [mainurl]

    for i in range(0,9):
        new_url = 'https://finviz.com/screener.ashx?v=152&ft=4&o=-marketcap&r=' + str(((i*20) + 21)) + '&c=0,1,3,4,5,6,7,9,11,13,16,17,27,33,34,37,51,67,65,66'
        url_list.append(new_url)
    
    return url_list

def getTable():
    try:
        url_list = generateUrls()
        table = []

        for each in url_list:

            request = Request(url=each,headers={'user-agent': 'stock_screener'}) 
            response = urlopen(request)

            # Use beautiful soup to get html form webpage
            html = BeautifulSoup(response, features="lxml")

            # Get news table from each ticker site and store in list
            row_list = html.findAll('tr', class_='styled-row is-hoverable is-bordered is-rounded is-striped has-color-text')

            for row in row_list:
                a_list = row.findAll('a')

                values = []
                for value in a_list:
                    values.append(value.text)

                table.append(values) 

            time.sleep(0.1)   

        # Get column titles
        request = Request(url=each,headers={'user-agent': 'stock_screener'}) 
        response = urlopen(request)
        html = BeautifulSoup(response, features="lxml")
        title_bar = html.find('tr', align='center', valign='middle')
        titles = title_bar.findAll('th')
        column_titles = []
        for value in titles:
            column_titles.append((value.text).strip())
        df = pd.DataFrame(table, columns=column_titles)    

    except KeyError:
        pass

    return df

def screen():
    # url = addCriteria()
    df = getTable()

    print(df)

    return df
