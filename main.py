import requests as r
import pandas as pd 


url = "https://mboum-finance.p.rapidapi.com/v1/markets/stock/modules"
print("Insert stock to find out its facts: ")
querystring = {
    "symbol": input(),
    "module": "financial-data"
}

headers = {
    "X-RapidAPI-Key": "237fc3aabcmsh0e29536d4aadfefp185f32jsnc8ad5dd36988",
    "X-RapidAPI-Host": "mboum-finance.p.rapidapi.com"
}

    
response = r.get(url, headers=headers, params=querystring)
print(response.json()['body']['currentPrice'])
        
