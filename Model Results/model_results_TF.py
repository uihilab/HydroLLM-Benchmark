import openai
from sklearn.metrics import accuracy_score
import pandas as pd
import csv
import requests
import os

api_key = os.getenv("OPENAIAPI")
openai.api_key = api_key

url = os.getenv("URL")

TF_data = pd.read_csv("")

def model_answer(question, model):
    prompt = f"""
    Your task is to perform the following actions.

    1.	Read the Statement: Review the statement enclosed within triple backticks (```).
	2.	Determine the Truthfulness: Assess whether the statement is True or False.
	3.	Respond Appropriately: Return only True or False, without any additional text or explanation.

    Statement to Evaluate:: ```{question}```
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in answering True or False questions with high accuracy. Your task is to read the provided statement, determine whether it is **True** or **False**, and respond with **only** the word `True` or `False` without any additional text, explanations, or formatting."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100,   
    )

    return response.choices[0].message.content


def llama_results(question):
    prompt = f"""
    Your task is to perform the following actions.

    1.	Read the Statement: Review the statement enclosed within triple backticks (```).
	2.	Determine the Truthfulness: Assess whether the statement is True or False.
	3.	Respond Appropriately: Return only True or False, without any additional text or explanation.

    Statement to Evaluate:: ```{question}```
        """

    messages = [
        {"role": "system", "content": "You are an expert in answering True or False questions with high accuracy. Your task is to read the provided statement, determine whether it is **True** or **False**, and respond with **only** the word `True` or `False` without any additional text, explanations, or formatting."},
        {"role": "user", "content": prompt},
            ]

    url = url

    data = {
        "model": "llama3:8b",
        "messages": messages,
        "stream": False
        }
    response = requests.post(url, json=data, verify=False)
    jsonres = response.json()
    

    return jsonres['message']['content']



for i in range(len(TF_data['Question'])):
    #model_response = model_answer(TF_data['Question'][i], "gpt-4o-mini")

    model_response = llama_results(TF_data['Question'][i])
    TF_data.loc[i, "llama3:8b"] = model_response

print(TF_data.head())

TF_data.to_csv("", index=False)
