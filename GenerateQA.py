import openai
import pandas as pd
import csv

openai.api_key = ""

chapter_dataset = pd.read_csv("Resources/FundamentalsOfHydrology_Chapters.csv")

def generate_qa(question_type, text):
    prompt = f"""
Generate 20 different ‘{question_type}’ questions based on the overall content of the following text:

‘{text}’

Only generate ‘{question_type}’ questions. Do not produce different types of questions.

The questions should focus on key ideas, themes, or concepts without referencing specific sections or chapters. In addition to the questions, generate 3 answers (A, B, C) for each question, with 2 incorrect and one correct answer. Also, provide a true open-ended answer in addition to those 3 answers. Finally, provide the text which you are generating the questions and answers from. You should give context for each question and provide 2 exact sentences from the text as context.

When producing the “Answer:”, your only allowed action is to copy and paste one of the answer choices (A, B, or C) exactly. You are not allowed to generate or modify the correct answer. You must pick the correct answer from the given options and copy-paste it without rewording, paraphrasing, or altering.

If the correct answer is not copied exactly from A, B, or C, return “Error: The correct answer was modified.”

The format must be as follows for each question:

Question:
A)
B)
C)
Answer: <copy-paste the exact correct answer sentence from A, B, or C>
Open Answer:
Context:

Always give the the Question, A), B), C), Answer, Open Answer and Context in different lines. Do not write them in the same line. 

Only provide the needed results next to each format category. Do not give it in a new line.

    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates questions from the given text and their answers as well as the correct answer, open ended answer, and the context which you generated the questions and answers."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )

    return response.choices[0].message.content

question_types = ["What", "How", "Where", "When", "How much", "Why"] #"How many" and "Whose questions were eliminated because they give results that are not suitable for the benchmark

answers = []
correct_answers = []
entire_answers = []
question = ""
correct_answer = ""
open_answer = ""
context = ""
letter = ""

with open("dataset.csv", mode="w", newline="") as file:
  writer = csv.writer(file)
  writer.writerow(["Question", "Answers", "Correct Answer", "Answer Letter", "Open Ended Answer", "Context"])


  for question_type in question_types:
    for index, row in chapter_dataset.iterrows():

      text = row["Text"]

      qGenerated = generate_qa(question_type, text)
      print(qGenerated)

      split = qGenerated.split("\n")
      print("----splitted version-------")
      print(split)
      print("---------------------------")

      current_answers = []

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

          writer.writerow([question, all_answers, correct_answer, letter, open_answer, context])

          answers = []
          current_answers = []

