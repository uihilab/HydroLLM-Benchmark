import openai
import csv
from secret import OPENAI_API_KEY
import pandas as pd

openai.api_key = OPENAI_API_KEY

book_data = pd.read_csv("")

def generate_FITB(text):
    
    prompt = f"""
        Your task is to perform following actions. 

        1. **Content Selection:**
        - Read the following text enclosed by triple backticks. This text is extracted from a book.
        - Focus solely on the main content of the text.

        2. **Question Generation:**
        - Based on the main content, generate **20 different fill in the blank questions** that cover the key topics and concepts discussed in the text. 
        - **Do not** reference specifics such as locations, times, or use phrases like "in this book," "the authors," "this topic," etc.       
        - Ensure that questions are **self-contained** and **standalone**, meaning they do not require external context to be understood.
        - **Do not** generate questions other than fill in the blank questions. 

        3. **Answer Options:**
        - The answer should be open and clear. 

        **Text to generate questions and answers:  ```{text}```**

        **Use the following format:**

        Question: <question>
        Answer: <answer>

        **Additional Instructions:**

        - **Clarity and Precision:** Ensure that questions are clear, precise, and free from ambiguity.

        - **Do Not Number the Questions:** Present the questions in the specified format without numbering them.

        - **Question format:** Only provide the needed results next to each format category. Give question and the answer in different lines. 

    """

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



with open("", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Question", "Answer"])
    file.flush()

    for i in range(len(book_data['Text'])):
        book_text = book_data['Text'][i]
        generated_qa = generate_FITB(book_text)
        print(generated_qa)
        print("---------------------------------")

        split = generated_qa.split("\n")
        print(split)

        question = None
        answer = None

        for line in split:
            if line.startswith("Question:"):
                question = line.replace("Question:", "").strip()
            elif line.startswith("Answer:"):
                answer = line.replace("Answer:", "").strip()
                if question and answer:
                    writer.writerow([question, answer])
                    file.flush()  
                    question = None
                    answer = None