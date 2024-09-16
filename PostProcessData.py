import openai
import pandas as pd
import csv

openai.api_key = ""

question_dataset = pd.read_csv("/Users/dilarakizilkaya/Desktop/HydroQA/dataset_1.csv")
chapter_text = pd.read_csv("Resources/FundamentalsOfHydrology_Chapters.csv")
test = pd.read_csv("/Users/dilarakizilkaya/Desktop/HydroQA/dataset_old.csv")

#Question check
def check_qa(question):
    prompt = f"""
    Is the question {question} a general question or does it contain specifics like years and locations? If it does, return yes, if it doesnt return no. 
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a question fixer, if there is a wrong formatted question, you fix it."},
            {"role": "user", "content": prompt}
        ],
        temperature =0.7,
        max_tokens = 500
    )

    return response.choices[0].message.content


#To replace the old  question with a new one
def generate_qa(text, question_dataset):
    prompt = f"""
    Generate 1 question based on the overall content of the following text:

    {text}

    The question should focus on key ideas, themes, or concepts without referencing specifics such as years and locations or names. In addition to the questions, generate 3 answers (A, B, C) for each question, with 2 incorrect and one correct answer. Also, provide a true open-ended answer in addition to those 3 answers. Finally, provide the text which you are generating the questions and answers from. You should give context for each question and provide 2 exact sentences from the text as context.

    When producing the “Answer:”, your only allowed action is to copy and paste one of the answer choices (A, B, or C) exactly. You are not allowed to generate or modify the correct answer. You must pick the correct answer from the given options and copy-paste it without rewording, paraphrasing, or altering.

    If the correct answer is not copied exactly from A, B, or C, return “Error: The correct answer was modified.”

    The format must be as follows for the question:

    Question:
    A)
    B)
    C)
    Answer: <copy-paste the exact correct answer sentence from A, B, or C>
    Open Answer:
    Context:    

    Always give the the Question, A), B), C), Answer, Open Answer and Context in different lines. Do not write them in the same line. 

    Only provide the needed results next to each format category. Do not give it in a new line.

    The question should be different than the questions in the dataset {question_dataset}

    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates a question from the given text and it's answers as well as the correct answer, open ended answer, and the context which you generated the question and answers."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )

    return response.choices[0].message.content


for question in test["Question"]:
    if check_qa(question) == 'Yes.':
        rows_to_drop = test[test["Question"] == question].index
        print(f"TEST: ----- YES {question} --- {rows_to_drop}")
        test = test.drop(rows_to_drop)

