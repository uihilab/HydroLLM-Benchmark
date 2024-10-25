import openai
import csv
from secret import OPENAI_API_KEY
import pandas as pd

openai.api_key = OPENAI_API_KEY

article_data = pd.read_csv("")

def generate_FITB(text):
    
    prompt = f"""
        Your task is to perform following actions. 

        1. **Content Selection:**
        - Read the following text enclosed by triple backticks. This text is extracted from a scientific article.
        - **Exclude** any content from the abstract and references sections.
        - Focus solely on the main content of the article.

        2. **Question Generation:**
        - Based on the main content, generate **20 open ended questions** that cover the key topics and concepts discussed in the article.
        - **Do not** reference specifics such as locations, times, or use phrases like "in this study," "the authors," "this research," etc.
        - Ensure that questions are **self-contained** and **standalone**, meaning they do not require external context to be understood.
        - The answer can't be longer than one sentence. Provide the answer in either words or a sentence. 
        - **Do not** generate a question other than the open ended question. 

        3. **Answer Options:**
        - The answer should be open and clear. 

        **Text to generate the question and answer:  ```{text}```**

        **Use the following format:**

        Question: <question>
        Answer: <answer>

        **Additional Instructions:**

        - **Avoid Specific Phrases:** Do not use phrases that tie the question to the article or study context, such as:
            - "In this study,"
            - "The authors found,"
            - "This research indicates,"
            - "According to the article,"
            - "The paper discusses,"

        - **Maintain Generality:** The questions should be applicable to the broader field or topic without referencing the source material.

        - **Clarity and Precision:** Ensure that the questions and the answers are clear, precise, and free from ambiguity.

        - **Do Not Number the Question:** Present the questions in the specified format without numbering.

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

    for i in range(0, len(article_data['Text'])):
        article_text = article_data['Text'][i]
        generated_qa = generate_FITB(article_text)
        print(generated_qa)
        print("---------------------------------")

        split = generated_qa.split("\n")
        print(split)

        question = None
        answer = None

        for line in split:
            if line.startswith("Question:") and question is None:
                question = line.replace("Question: ", "").strip()
            elif line.startswith("Answer:") and answer is None:
                answer = line.replace("Answer: ", "").strip()

            if question and answer:
                writer.writerow([question, answer])
                file.flush()

                question = None
                answer = None

            