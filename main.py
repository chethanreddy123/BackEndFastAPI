import re
import math
from collections import Counter
from urllib import request
import pandas as pd
from fastapi import FastAPI, Request, Query
from typing import Optional
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.encoders import jsonable_encoder
#import requests
import joblib



def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    word = re.compile(r'\w+')
    words = word.findall(text)
    return Counter(words)


def get_result(content_a, content_b):
    text1 = content_a
    text2 = content_b

    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    cosine_result = get_cosine(vector1, vector2)
    return cosine_result

from fast_autocomplete import AutoComplete
import pickle

open_file = open('sample.pkl', "rb")
loaded_list = pickle.load(open_file)
open_file.close()

words = {i : {} for i in loaded_list}
autocomplete = AutoComplete(words=words)


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/getInformation")
async def getInformation(info : Request):

    print(await info.body())

    req_info = await info.json()
    CurrString = dict(req_info)["SearchedString"]
    Results = []

    
    CurrString = autocomplete.search(word = CurrString, max_cost=3, size=1)[0][0]
    print(CurrString)

   

    model = joblib.load('model_joblib')

    TypeOf = model.predict([CurrString])
    print(TypeOf)

    k = TypeOf

    Ty = None

    if k == 0 :
        data = pd.read_csv('2W Keywords - 2W.csv')
        ListofAllWords = list(data.SearchedWord)
        Ty = "2 wheeler"
        #print(ListofAllWords)
    if k == 1:
        data = pd.read_csv('4W Keywords - 4W.csv')
        ListofAllWords = list(data.SearchedWord)
        Ty = "4 wheeler"
        #print(ListofAllWords)
    if k == 2:
        data = pd.read_csv('Brand Keyterms - Brand Keyterms.csv')
        ListofAllWords = list(data.SearchedWord)
        Ty = "Brand Key"
        #print(ListofAllWords)
    if k == 3:
        data = pd.read_csv('Health Keywords - Health.csv')
        ListofAllWords = list(data.SearchedWord)
        Ty = "health"
        #print(ListofAllWords)
    if k == 4:
        data = pd.read_csv('Travel Keywords - Travel.csv')
        ListofAllWords = list(data.SearchedWord)
        Ty = "travel"
        #print(ListofAllWords)
    if k == 5:
        data = pd.read_csv('Commercial.csv')
        ListofAllWords = list(data.SearchedWord)
        Ty = "Commercial"
        #print(ListofAllWords)
    if k == 6:
        data = pd.read_csv('cyber.csv')
        ListofAllWords = list(data.SearchedWord)
        Ty = "cyber"
        #print(ListofAllWords)
    if k == 7:
        data = pd.read_csv('Home Keywords.csv')
        ListofAllWords = list(data.SearchedWord)
        Ty = "Home"
        #print(ListofAllWords)
    if k == 8:
        data = pd.read_csv('Pet Keywords.csv')
        ListofAllWords = list(data.SearchedWord)
        Ty = "Pet"
        #print(ListofAllWords)

    

    def No_to_Type(number : int):
        if number == 0: return "https://www.bajajallianz.com/motor-insurance/two-wheeler-insurance-online/buy-online.html?src=CBM_02671&utm_source=GoogleBrand&utm_medium=cpc&param1=Brand_Bike_Insurance-N&param2=Bajaj_Bike_Ins+Exact&param3=bajaj%20bike%20insurance&utm_content=SEM&gclid=CjwKCAjw5NqVBhAjEiwAeCa97cB-jZ2RBH9jl6bg7MVApdNkZ5Zvq7YzOQXSXFuhXqBpfwdPkusGgBoCOdUQAvD_BwE&gclsrc=aw.ds" 
        if number == 1: return "https://www.bajajallianz.com/motor-insurance/car-insurance-online/buy-online.html?src=CBM_02671&utm_source=GoogleBrand&utm_medium=cpc&param1=Brand_Desktop_Top14Location_Apr%2720_RLSA&param2=Brand%204%20Wheeler%20Ins&param3=bajaj%20allianz%204%20wheeler%20insurance&utm_content=SEM&gclid=CjwKCAjw5NqVBhAjEiwAeCa97fI0MAp5VyGIirYEWIWp2uyiEiRRbb2VcM_C8fvSOcAyLOjrLKwe_hoCtgEQAvD_BwE&gclsrc=aw.ds"
        if number == 2: return "https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwiO6NiLy8n4AhWommYCHeMMBNUYABAAGgJzbQ&ohost=www.google.com&cid=CAESbOD2Hz3-OFW0c_OGLTqGWsuK3Xpa5uZWOi9Phk0YQlseNnG49YruFfaWCIQtKIIeHki3p6u1maPnSOnO_dUl7-d9oPUAmxW4FFCoxNJIXlA1h6RlmHhhY2YeIYNk27jOsYJrgjUfP80mjcxztw&sig=AOD64_2QU7jjds02Rt8BBDcsW0t4liXimg&q&adurl&ved=2ahUKEwjSwNGLy8n4AhXBSmwGHZW8CqcQ0Qx6BAgEEAE"
        if number == 3: return "https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwj7hr66y8n4AhXJg0sFHb03DkMYABABGgJzZg&ohost=www.google.com&cid=CAESbOD2bx0DZdDhNg4FOLp2NMTmxf2oJWdMMMr-Aq8HLZe1sskdkNct5aSBAkc0PMFx9MUkyUoLtj20Q-DXPUH3Q-EaHYMfddbx1Q42ce7BGwkrmIcPXoNKDndiuJOsWDqOaTcLjlmy3xNytkGOdg&sig=AOD64_2tkoean-AjH6tXMnnJq1BBPEgCQA&q&adurl&ved=2ahUKEwjEprW6y8n4AhX01jgGHZAQC9cQ0Qx6BAgFEAE"
        if number == 4: return "https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwiNr7PIy8n4AhWYmGYCHXDPABAYABAAGgJzbQ&ohost=www.google.com&cid=CAESbOD27_ASot0N-ToNkK7_2w7a61e-evrK9MEf9KvFMGEf0NnN0Clw-OR1g3Jg-yJoMTzGWm8dtHtBp7cobdhnHJoknmcq5hbuo2r3PxhEB5EbH1JtA8NUhM7hK-oZo6EGZ1c5Ao830So5nCMfzA&sig=AOD64_1quSStodgDTnBgzt8paQZx_NOWZA&q&adurl&ved=2ahUKEwjs9qvIy8n4AhWw2TgGHWrZAaQQ0Qx6BAgDEAE"
        if number == 5: return "https://www.bajajallianz.com/commercial-insurance.html"
        if number == 6: return "https://www.bajajallianz.com/cyber-insurance.html"
        if number == 7: return "https://www.bajajallianz.com/home-insurance.html"
        if number == 8: return "https://www.bajajallianz.com/general-insurance.html?utm_source=GoogleBrandBagic&param1=Enhanced_Sitelink&param2=Enhaced_Site_Link&param3=bajaj%20allianz&utm_content=SEM&gclid=CjwKCAjw5NqVBhAjEiwAeCa97T7gR6GFiFTp4qt7xJ_bozTONMjy2QJ4hN5-h5xMXVEkcK56ROS6BBoC0r4QAvD_BwE&gclsrc=aw.ds"

    for mainWords in ListofAllWords:
        if get_result(mainWords,CurrString) > 0.3:
            finalString = ""
            for i in mainWords:
                if i.isalpha() == True or i.isspace() ==  True:
                    finalString += i
            
            Results.append({"text" : finalString , "link" : No_to_Type(k), "type" : Ty})

    
    D = {
        "SearchResults" : Results
    }
    

    return jsonable_encoder(D)