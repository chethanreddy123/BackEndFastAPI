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

data = pd.read_csv('SearchWords.csv')
ListofAllWords = list(data.Keywords)

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

    req_info = await info.json()
    CurrString = dict(req_info)["SearchedString"]
    Results = []
    

    for mainWords in ListofAllWords:
        if get_result(mainWords,CurrString) > 0.3:
            finalString = ""
            for i in mainWords:
                if i.isalpha() == True or i.isspace() ==  True:
                    finalString += i
            Results.append(finalString)

    
    D = {
        "SearchResults" : Results
    }
    

    return jsonable_encoder(D)
