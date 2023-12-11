from sentiment import sentiment
from screen import screen
import pandas as pd

from firebase_admin import db
import firebase_admin
from firebase_admin import credentials

def firebaseSetup():
    cred = credentials.Certificate("keys/credentials.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://stockscreener-b26db-default-rtdb.firebaseio.com/'
    })


def loadDatabase(df):

    firebaseSetup()

    # Get a reference to the root of your database
    ref = db.reference('/')

    # Push your data to the database
    new_data_ref = ref.push(df)

    # Return the unique key generated for this data
    return new_data_ref.key

if __name__ == "__main__":
    df = screen()
    tickers = df.iloc[:, 1].tolist()
    raw, sentiment_values = sentiment(tickers)

    result = pd.concat([df, sentiment_values['Sentiment']], axis=1)

    unique_key = loadDatabase(result.to_json(orient='index'))

    print(unique_key)