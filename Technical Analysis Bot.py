import yfinance as yf
import pandas as pd
from datetime import timedelta, date

today = date.today()
def days_ago(n):
  return (date.today() - timedelta(n)).strftime('%Y-%m-%d')

ticker = "TSLA"
start_date = days_ago(30) # or replace with any number of days you want. Note, Yahoo Finance will 
                          # only work with data in the last sixty days. 
                          
end_date = today.strftime('%Y-%m-%d')
dataF = yf.download(ticker, start_date, end_date, interval='1d')
dataF.iloc[:,:]

dataF_string = dataF.to_string()

import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# Convert the DataFrame to a string
dataF_string = dataF.to_string()

# Create a prompt
messages = [
    {
        "role": "system",
        "content": """You are a world class financial analyst. You excel at observing bullish and 
                    bearish technical analysis trends in past stock data."""
    },
    {
        "role": "user",
        "content": f"""The following stock data for TSLA was retrieved:\n{dataF_string}\nPlease 
        provide an analysis of the trend and make suggestions on how a trader should position in 
        the short term to maximize profitability. Point out any bullish or bearish patterns such 
        as bull flag, bear flag, cup and handle, or other technical analysis patterns."""
    }
]

# Make the API call
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", # You can use this engine or another available GPT-3 engine
  messages=messages,
  max_tokens=1000
)

# The response will include the model's generated text
generated_text = response.choices[0].message['content']

print(generated_text)
