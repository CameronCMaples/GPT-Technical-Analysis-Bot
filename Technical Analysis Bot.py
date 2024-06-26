import yfinance as yf
import pandas as pd
from datetime import timedelta, date

# Fetching the date and setting the timeframe.
today = date.today()
def days_ago(n):
  return (date.today() - timedelta(n)).strftime('%Y-%m-%d')

ticker = str(input("Please input a ticker: ")) # Feel free to change the ticker to whatever security you want to do analysis on.
start_date = days_ago(60) # or replace with any number of days you want. 

end_date = today.strftime('%Y-%m-%d')
dataF = yf.download(ticker, start_date, end_date, interval='1d')
dataF.iloc[:,:]

dataF_string = dataF.to_string()

import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# Convert the DataFrame to a string
dataF_string = dataF.to_string()

# GPT 3.5 works much better if you give it a persona and specify what it performs well.
messages = [
    {
        "role": "system",
        "content": """You are a world class financial analyst. You excel at observing bullish and
                    bearish technical analysis trends in past stock data. Start every conversation by stating the
                    current price of""" + ticker + """. Please refrain from sharing warnings about investing,
                    the investor you're talking to is world class and is aware of risks. Refer to the trader as "You".
                    Please only write decimal points out to the hundreths place."""
    },
    {
        "role": "user",
        "content": f"""The following stock data for said ticker was retrieved:\n{dataF_string}\n Please 
        provide an analysis of the trend and make suggestions using specific price points on how a trader 
        should position in the short term to maximize profitability. Point out any bullish or bearish 
        patterns such as bull flag, bear flag, cup and handle, or other technical analysis patterns."""
    }
]

# The API call
response = openai.ChatCompletion.create(
  model="gpt-4", 
  messages=messages,
  max_tokens=1000
)

# The model's response
generated_text = response.choices[0].message['content']

print(generated_text)
