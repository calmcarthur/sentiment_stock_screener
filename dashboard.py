import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

from firebase_admin import db
import firebase_admin
from firebase_admin import credentials

def firebaseSetup():
    cred = credentials.Certificate("keys/credentials.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://stockscreener-b26db-default-rtdb.firebaseio.com/'
    })

st.title('Sentiment Stock Screener')

def fetchTop():
    if not firebase_admin._apps:
        firebaseSetup()
    
    ref = db.reference('/')

    top = ref.order_by_key().limit_to_last(1).get()
    key = list(top.keys())
    data = top[key[0]]

    df = pd.read_json(StringIO(data), orient='index')
    return df

if __name__ == "__main__":
    data_load_state = st.text('Loading data...')   
    df = fetchTop()
    data_load_state.text("Done")

    if st.checkbox('Show The Data'):
        st.subheader('The Data')
        st.write(df)


    
