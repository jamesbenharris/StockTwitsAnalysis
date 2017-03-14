#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 20:03:43 2017

@author: Ben Harris
@email: james.ben.harris@gmail.com
"""
import sys
import requests
import re
import json
import psycopg2
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def clean(text):
    text = re.sub("[0-9]+", "number", text)
    text = re.sub("#", "", text)
    text = re.sub("\n", "", text)
    text = re.sub("$[^\s]+", "", text)
    text = re.sub("@[^\s]+", "", text)
    text = re.sub("(http|https)://[^\s]*", "", text)
    text = re.sub("[^\s]+@[^\s]+", "", text)
    text = re.sub('[^a-z A-Z]+', '', text)
    return text

def score(text):
    return SentimentIntensityAnalyzer().polarity_scores(text)["compound"]

def sentiment(message):
    try:
        msg = message['entities']['sentiment']['basic']
        if msg == "Bullish":
            msg = 1
        else:
            msg = -1
    except:
        msg = 0
    return msg

def writeToDatabase(server, db, table, un, pwd, ticker, sentiment, source):
    #try:
        connection_string = "host='%s' dbname='%s' user='%s' password='%s'" % (server,db,un,pwd)
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        query = "insert into %s (source,ticker,sentiment,market) values ('%s','%s',%.3f,'%s')" % (table,source, ticker, sentiment, 'SP500')
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
    #except:
    #    print("Unexpected error:", sys.exc_info()[0])

def query(ticker):
    url = "https://api.stocktwits.com/api/2/streams/symbol/%s.json?limit=30"%(ticker)
    response = requests.get(url)
    return json.loads(response.text)

def getAVGSentiment(ticker):
    data = query(ticker)
    sum_score = 0
    length = len(data['messages'])
    for message in data['messages']:
        text = clean(message['body'])
        sent = sentiment(message)
        sc = score(text)
        weighted_score = (sc+sent)/2
        sum_score += weighted_score
    avg_score = round(sum_score/length,3)
    return avg_score

def analyze(tickers):
    for ticker in tickers:
        print(getAVGSentiment(ticker))

def storeAnalysis(db,tickers):
    for ticker in tickers:
        writeToDatabase(db[0],db[1],db[2],db[3],db[4],ticker,getAVGSentiment(ticker),'StockTwits')
    return 'Success'


