import pandas as pd
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from secret import OPENAI_API_KEY
import requests

openai.api_key = OPENAI_API_KEY 

df = pd.read_csv('')

def gpt_result(question, model):
    prompt = f"""
    Your task is to perform the following actions.

    1.	Read the Question: Review the question enclosed within triple backticks (```).
	2.	Answer the question in 2 or 3 sentences. Do not answer it any longer than 2-3 sentences.
	3.	Return your answer

    Question to Complete: ```{question}```

    """
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in answering questions with high accuracy. Your task is to read the provided question, answer it, and supply the correct answer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000,  
    )

    return response.choices[0].message.content

def llama_result(question):
    prompt = f"""
    Your task is to perform the following actions.

    1.	Read the Question: Review the question enclosed within triple backticks (```).
	2.	Answer the question in 2 or 3 sentences. Do not answer it any longer than 2-3 sentences.
	3.	Only return the answer, do not return anything else. 

    Question to answer: ```{question}```    
    """

    messages = [
    {"role": "system", "content": "You are an expert in answering questions with high accuracy. Your task is to read the provided question, answer it, and supply the correct answer."},
    {"role": "user", "content": prompt},
    ]

    url = "https://r-uihilab01.ecn.uiowa.edu/ollama/api/chat"

    data = {
        "model": "llama3.1:70b",
        "messages": messages,
        "stream": False
    }
    response = requests.post(url, json=data, verify=False)
    jsonres = response.json()
    

    return jsonres['message']['content']



def get_embedding(text, model="text-embedding-3-large"):
   text = text.replace("\n", " ")
   return openai.embeddings.create(input = [text], model=model).data[0].embedding


for i in range(0, len(df['Question'])):

    model_result = llama_result(df['Question'][i])
    print(df['Answer'][i])
    print("--------------------------------------------------")
    print(model_result)
    print("--------------------------------------------------")
    df.loc[i, "llama3.1:70b"] = model_result

    embedding1 = get_embedding(model_result)
    embedding2 = get_embedding(df['Answer'][i])

    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)

    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)

    similarity = cosine_similarity(embedding1, embedding2)[0][0]

    print(similarity)

    df.loc[i, "similarity_llama3.1:70b"] = similarity

    print("---------------------------------------------------")

print(df.head())

df.to_csv("", index=False)







