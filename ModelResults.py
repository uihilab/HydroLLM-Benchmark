import openai
from secret import OPENAI_API_KEY
import pandas as pd
from sklearn.metrics import accuracy_score
import transformers
import torch
import requests

openai.api_key = OPENAI_API_KEY

df = pd.read_csv("/Users/dilarakizilkaya/Desktop/HydroQA/test3.csv")

df_QA = df[['Question', 'Answers']]

#print(df_QA.head())

def model_answers(question, answers, model):
    prompt = f"""
    From the given question: {question}, choose the correct answer from the options: {answers}. 
    Return only the answer letter without any additional text and return only 1 answer.
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in answering multiple-choice questions accurately."},
            {"role": "user", "content": prompt}
        ],
        #temperature=0.7,
        #max_tokens=20
        #o1 mini
        #messages=[
        #{"role": "user", "content": prompt}
  #]


        #llama

        
    )

    return response.choices[0].message.content

def llama_results(question, answers):
    prompt = f"""
    From the given question: {question}, choose the correct answer from the options: {answers}. 
    Return only the answer letter (e.g., A, B, C) without ")" and any additional text Return only 1 answer.
    """

    messages = [
    {"role": "system", "content": "You are an expert in answering multiple-choice questions accurately."},
    {"role": "user", "content": prompt},
    ]

    url = ""

    data = {
        "model": "llama3.1:70b",
        "messages": messages,
        "stream": False
    }
    response = requests.post(url, json=data)
    jsonres = response.json()
    

    return jsonres['message']['content']



for i in range(len(df['Question'])):
    #model_response = model_answers(df['Question'][i], df['Answers'][i], "gpt-4o")

    model_response = llama_results(df['Question'][i], df['Answers'][i])
    df.loc[i, "llama3.1-70b"] = model_response

print(df.head())

df.to_csv(".csv", index=False)

#result_df = pd.read_csv("/Users/dilarakizilkaya/Desktop/HydroQA/test.csv")

#accuracy_gpt4omini = accuracy_score(result_df['Answer Letter'], result_df['gpt-4o-mini'])

#print(f'Accuracy: {accuracy_gpt4omini:.4f}')








