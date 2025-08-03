import yfinance as yf
import pandas as pd
import pytz
from datetime import datetime, date, timedelta
import pandas_market_calendars as mcal
import requests
import json

# Time and date setup
now = datetime.now(pytz.timezone("US/Eastern"))
today = date.today()

# Set up API access
API_KEY = ''
url = "https://openrouter.ai/api/v1/chat/completions"

# Download QQQ data
qqq = yf.Ticker("QQQ")
news = qqq.news

# Get 5-min candles from yesterday only
nyse = mcal.get_calendar("XNYS")
schedule = nyse.schedule(start_date=today - timedelta(days=7), end_date=today)
yesterday = schedule.index[-2].date()  # previous market day

qqq_data = yf.download("QQQ", start=yesterday, end=yesterday + timedelta(days=1), interval="5m")

# Keep only first and last 5 candles
qqq_data = qqq_data.reset_index()
qqq_data.columns = [str(col) for col in qqq_data.columns]
def serialize_candles(candles):
    for row in candles:
        for key, value in row.items():
            if isinstance(value, pd.Timestamp):
                row[key] = value.isoformat()
    return candles

first5 = serialize_candles(qqq_data.head(5).to_dict(orient="records"))
last5 = serialize_candles(qqq_data.tail(5).to_dict(orient="records"))
qqq_data_json = first5 + last5

# Clean news
cleaned_news = []
for item in news:
    c = item.get("content", {})
    cleaned_news.append({
        "title": c.get("title"),
        "summary": c.get("summary"),
        "url": c.get("clickThroughUrl", {}).get("url"),
        "source": c.get("provider", {}).get("displayName"),
        "published": c.get("pubDate")
    })

# Prompt for model
prompt = (
    "DONT FORMAT OUTPUT. USE REASON BUT DONT SHOW IT. THIS IS FOR API CALL I NEED CLEAN OUTPUT. "
    "Role-play as a professional trader. you are working on QQQ. you will receive first and last 5 candles "
    "of yesterday and before market opens news. you will read the articles and tag them considering the candles "
    "in 'bull' 'bear' or 'neutral'. Consider that QQQ is strictly related to the S&P500 and general market heading, "
    "so news regarding these are related to QQQ price movements. return an array compatible with python that has "
    "as the first item the number of analyzed articles, second item the number of articles flagged as bear, third number of bull, "
    "fourth number of neutral. DONT FORMAT THIS DATA. THIS IS FOR API CALL I NEED CLEAN OUTPUT. "
    "heres your candles:" + json.dumps(qqq_data_json) + " news:" + json.dumps(cleaned_news)
)
qw_prompt = (

    "DONT FORMAT OUTPUT. USE REASON BUT DONT SHOW IT. THIS IS FOR API CALL I NEED CLEAN OUTPUT. "
    "Role-play as a professional trader. you are working on QQQ. you will receive first and last 5 candles "
    "of yesterday and before market opens news. you will read the articles and tag them considering the candles "
    "in 'bull' 'bear' or 'neutral'. Consider that QQQ is strictly related to the S&P500 and general market heading, "
    "so news regarding these are related to QQQ price movements. return an array compatible with python that has "
    "as the first item the number of analyzed articles, second item the number of articles flagged as bear, third number of bull, "
    "fourth number of neutral. DONT FORMAT THIS DATA. THIS IS FOR API CALL I NEED CLEAN OUTPUT. "
    "Then, return only a Python array in the following format:  "
    " [number_of_articles, bear_count, bull_count, neutral_count]"
    "Do NOT explain your reasoning. Return only the array.  "
    "heres your candles:" + json.dumps(qqq_data_json) + " news:" + json.dumps(cleaned_news)
)



# Prepare headers and body
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "X-Title": "Bobby"
}

#qwen
data_q1 = {
    "model": "qwen/qwen3-14b:free", 
    "messages": [           
        {
            "role": "user",
            "content": prompt
        }
    ]
}


q1_response = requests.post(url, headers=headers, json=data_q1)
q1_response_json = q1_response.json()
q1_content = q1_response_json['choices'][0]['message']['content']


print("q1 result:\n")
print(q1_content+"\n")

#quenq
data_q2 = {
    "model": "qwen/qwq-32b:free", 
    "messages": [           
        {
            "role": "user",
            "content": prompt
        }
    ]
}

q2_response = requests.post(url, headers=headers, json=data_q2)
q2_response_json = q2_response.json()
q2_content = q2_response_json['choices'][0]['message']['content']

print("q2 result:\n")
print(q2_content+"\n")

#deepseek
data_d = {
    "model": "deepseek/deepseek-r1-0528:free", 
    "messages": [           
        {
            "role": "user",
            "content": qw_prompt
        }
    ]
}

d_response = requests.post(url, headers=headers, json=data_d)
d_response_json = d_response.json()
d_content = d_response_json['choices'][0]['message']['content']

print("deepseek result:\n")
print(d_content+"\n")


#zai
data_z = {
    "model": "z-ai/glm-4.5-air:free", 
    "messages": [           
        {
            "role": "user",
            "content": prompt
        }
    ]
}

z_response = requests.post(url, headers=headers, json=data_z)
z_response_json = z_response.json()
z_content = z_response_json['choices'][0]['message']['content']

print("z-ai result:\n")
print(z_content+"\n")



