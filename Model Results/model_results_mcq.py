import openai
import pandas as pd
from sklearn.metrics import accuracy_score
import transformers
import torch
import requests

api_key = os.getenv("OPENAIAPI")
openai.api_key = api_key

ollama_api = os.getenv("OLLAMA_API")

df = pd.read_csv("")

df_QA = df[['Question', 'Answers']]

def model_answers(question, answers, model):
    prompt = f"""
    Your task is to perform the following actions.

    1.	Read the Question: Review the question enclosed within triple backticks (```).
	2.	Answer the question and choose the correct answer letter from answer choices eclosed within trple backticks (```). Only answer using the answer letter.
	3.	Only return the correct answer letter, do not return anything else. 

    Question to answer: ```{question}```    
    Answer to choose: ```{answers}```  
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in answering questions with high accuracy. Your task is to read the provided question, answer it and choose the correct answer, and supply the correct answer letter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=20      
    )

    return response.choices[0].message.content

def llama_result(question, answers):
    prompt = f"""
    Your task is to perform the following actions.

    1.	Read the Question: Review the question enclosed within triple backticks (```).
	2.	Answer the question and choose the correct answer letter from answer choices eclosed within trple backticks (```). Only answer using the answer letter.
	3.	Only return the correct answer letter, do not return anything else, do not add ")" at the end of the answer letter. 

    Question to answer: ```{question}```    
    Answer to choose: ```{answers}```    
    """

    messages = [
    {"role": "system", "content": "You are an expert in answering questions with high accuracy. Your task is to read the provided question, answer it and choose the correct answer, and supply the correct answer letter."},
    {"role": "user", "content": prompt},
    ]

    url = ollama_api

    data = {
        "model": "llama3.1:70b",
        "messages": messages,
        "stream": False
    }
    response = requests.post(url, json=data, verify=False)
    jsonres = response.json()
    

    return jsonres['message']['content']
    


for i in range(len(df['Question'])):
    #model_response = model_answers(df['Question'][i], df['Answers'][i], "gpt-4o-mini")
    #print(model_response)

    model_response = llama_result(df['Question'][i], df['Answers'][i])
    print(model_response)
    df.loc[i, 'llama3.1:70b'] = model_response

print(df)

df.to_csv("", index=False)
