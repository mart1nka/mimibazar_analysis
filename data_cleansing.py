import requests
import json
import pandas as pd

with open("C:/Temp/recepty.json") as file:
    data = json.load(file)
for i in data:
    for key in i.keys():
        try:
            i[key] = i[key].replace('\\r', '').replace('\\n', '\n').replace('\\', '')
        except: 
            pass 

recepty = json.dumps(data, ensure_ascii=False, indent = 4)

df = pd.read_json(recepty)

df_10 = df[df['ingredients'].str.len() > 10]
df_10 = df[df['instructions'].str.len() > 10]

df_10.to_csv('out_all4.csv', encoding="utf-8")

nezdravy_recept = df_10[df_10['ingredients'].str.lower().str.contains("kečup") & df_10['ingredients'].str.lower().str.contains("tatar")]
nezdravy_recept