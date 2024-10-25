import openai
import csv
from secret import OPENAI_API_KEY
import pandas as pd

openai.api_key = OPENAI_API_KEY

data = pd.read_csv("")

prompt = """
    Your task is to perform the following actions.

    1. **Content Selection:**
        - Read the following text enclosed by triple backticks. This text is extracted from a scientific article.
        - **Exclude** any content from the abstract and references sections.
        - Focus solely on the main content of the article.

    2. **Question Generation:**
        - Based on the main content, generate **20 different insightful and general questions** that cover the key topics and concepts discussed in the article.
        - **Do not** reference specifics such as locations, times, or use phrases like "in this study," "the authors," "this research," etc.
        - Ensure that the questions are **self-contained** and **standalone**, meaning they do not require external context to be understood.

    3. **Answer Options:**
        - For the questions, generate **3 answer choices** labeled A, B, and C.
        - Ensure there is only **1 correct answer** among the options.
        - The incorrect answers (distractors) should be plausible to avoid obvious elimination.

    4. **Correct Answer Identification:**
        - Clearly indicate the correct answer by specifying the letter and the corresponding answer choice.

    **Text to generate questions and answers:  ```{text}```**

    **Use the following format:**

    Question: <Question>
    A) <Answer A>
    B) <Answer B>
    C) <Answer C>
    Answer: <True Answer Letter)> <True Answer Sentence>

    **Additional Instructions:**

        - **Avoid Specific Phrases:** Do not use phrases that tie the question to the article or study context, such as:
            - "In this study,"
            - "The authors found,"
            - "This research indicates,"
            - "According to the article,"
            - "The paper discusses,"

        - **Maintain Generality:** The question should be applicable to the broader field or topic without referencing the source material.

        - **Clarity and Precision:** Ensure that the question are clear, precise, and free from ambiguity.

        - **Do Not Number the Question:** Present the question in the specified format without numbering.
    """

def generateQA(text, prompt):

    prompt = prompt.format(text=text)

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert on generating questions and answers from the given article."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )

    return response.choices[0].message.content


answers = []
correct_answers = []
entire_answers = []
question = ""
correct_answer = ""
open_answer = ""
context = ""
letter = ""

with open("", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Question", "Answers", "Correct Answer", "Answer Letter", "Open Ended Answer"])
    file.flush()

    for i in range(0, len(data['Text'])):
        generated_question = generateQA(data['Text'][i], prompt)
        print(generated_question)
        split = generated_question.split("\n")
        print("----splitted version-------")
        print(split)
        print("---------------------------")
        
        current_answers = []

        for j in split:

            if j.startswith("Question:"):
                question = j.replace("Question: ", "").strip()
                current_answers = []

            elif j.startswith("A)") or j.startswith("B)") or j.startswith("C)"):
                current_answers.append(j.strip())

            elif j.startswith("Answer:"):

                if j.startswith("Answer: A"):
                    letter = "A"
                elif j.startswith("Answer: B"):
                    letter = "B"
                elif j.startswith("Answer: C"):
                    letter = "C"

                correct_answer = j.replace("Correct Answer: ", "").strip()

                all_answers = ", ".join(current_answers)

                writer.writerow([question, all_answers, correct_answer, letter, open_answer])
                file.flush()
                answers = []
                current_answers = [] 


            



        

    