import openai
from secret import OPENAI_API_KEY
import pandas as pd

openai.api_key = OPENAI_API_KEY

df = pd.read_csv("/Users/dilarakizilkaya/Desktop/HydroQA/datasets/HydoQA_dataset.csv")

df_QA = df[['Question', 'Answers']]

#print(df_QA.head())

def model_answers(question, answers, model):
    prompt = f"""
    From a given question {question}, choose the correct answer from {answers}. Return the correct answer in the format below:

    Answer: <answer letter> 

    """
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in answering multiple-choice questions accurately."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content

#df['gpt-4o-mini'] = None
for i in range(len(df['Question'])):
    model_response = model_answers(df['Question'][i], df['Answers'][i], "gpt-4o-mini")

    df.loc[i, "gpt-4o-mini"] = model_response

print(df.head())

df.to_csv("HydroQA_gpt4ominiResultsWithAnswerLetters.csv", index=False)