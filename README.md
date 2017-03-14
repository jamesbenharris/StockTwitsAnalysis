# StockTwitsAnalysis
# Example
# Import
import StockSentiment

# Variables
tickers = ['TSLA','SNAP','AAPL','AMZN','YHOO','GOOG']

# PostgreSQL Database Information
SERVER = 'localhost'
DATABASE = 'Stock'
TABLE = '"Sentiment"'
DB_UN = ''
DB_PWD = ''

# Store DB Information 
db = [SERVER,DATABASE,TABLE,DB_UN,DB_PWD]
# Execute Class
storeAnalysis(db,tickers)
