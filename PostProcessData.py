import openai
import pandas as pd
import csv

openai.api_key = ""

questions_path = ""
question_dataset = pd.read_csv("")
chapter_text = pd.read_csv("")
test = pd.read_csv("")

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
    Generate a question based on the overall content of the following text which should also different than the questions in {question_dataset}:

    {text}

    The question should focus on key ideas, themes, or concepts without referencing specifics such as years and locations or names. In addition to the questions, generate 3 answers (A, B, C) for each question, with 2 incorrect and one correct answer. Also, provide a true open-ended answer in addition to those 3 answers. Finally, provide the text which you are generating the questions and answers from. You should give context for each question and provide 2 exact sentences from the text as context.

    When producing the “Answer:”, your only allowed action is to copy and paste one of the answer choices (A, B, or C) exactly. You are not allowed to generate or modify the correct answer. You must pick the correct answer from the given options and copy-paste it without rewording, paraphrasing, or altering.

    If the correct answer is not copied exactly from A, B, or C, return “Error: The correct answer was modified.”

    The format must be as follows for the question:

    Question: <Question sentence>
    A) <Answer A>
    B) <Answer B>
    C) <Answer C> 
    Answer: <copy-paste the exact correct answer sentence from A, B, or C>
    Open Answer: <Open Answer>
    Context: <Context>

    Always give the the Question, A), B), C), Answer, Open Answer and Context in different lines. Do not write them in the same line. 

    Do not provide the category results in different lines, always provide them next to each format category. 

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



for question in question_dataset["Question"]:
    if check_qa(question) == 'Yes.':
        rows_to_drop = question_dataset[question_dataset["Question"] == question].index
        print(f"TEST: ----- YES {question} --- {rows_to_drop}")
        question_dataset = question_dataset.drop(rows_to_drop)

        generated_q = generate_qa(chapter_text["Text"][3], question_dataset)

        split = generated_q.split("\n")

        current_answers = []
        results = [None] * 6  
        
        for i in split:

            if i.startswith("Question:"):
                question = i.replace("Question: ", "").strip()
                current_answers = []

            elif i.startswith("A)") or i.startswith("B)") or i.startswith("C)"):
                current_answers.append(i.strip())

            elif i.startswith("Answer:"):

                if i.startswith("Answer: A"):
                    letter = "A"
                elif i.startswith("Answer: B"):
                    letter = "B"
                elif i.startswith("Answer: C"):
                    letter = "C"

                correct_answer = i.replace("Correct Answer: ", "").strip()

            elif i.startswith("Open Answer:"):
                open_answer = i.replace("Open Answer: ", "").strip()

            elif i.startswith("Context:"):
                context = i.replace("Context: ", "").strip()

        #print(letter)

                all_answers = ", ".join(current_answers)

                results[0] = question
                results[1] = all_answers
                results[2] = correct_answer
                results[3] = letter
                results[4] = open_answer
                results[5] = context

                new_data = pd.DataFrame([results], columns=["Question", "Answers", "Correct Answer", "Answer Letter", "Open Ended Answer", "Context"])

                question_dataset = question_dataset._append(new_data, ignore_index=True)

                print("-----------------------")
                print(split)
                print("-----------------------")
                print("New rows added successfully.")

                answers = []
                current_answers = []
   
question_dataset = question_dataset[question_dataset[["Question", "Answers", "Correct Answer", "Answer Letter", "Open Ended Answer", "Context"]].notna().all(axis=1)]

question_dataset.to_csv('output_file.csv', index=False)
