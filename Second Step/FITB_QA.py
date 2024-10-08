import openai
import csv
from secret import OPENAI_API_KEY
import pandas as pd

openai.api_key = OPENAI_API_KEY

article_data = pd.read_csv("/Users/dilarakizilkaya/Desktop/HydroQA/Second Step/elsevier_articles_full_text_final1.csv")

def generate_FITB(text):
    
    prompt = f"""
        Your task is to perform following actions. 

        1. **Content Selection:**
        - Read the following text enclosed by triple backticks. This text is extracted from a scientific article.
        - **Exclude** any content from the abstract and references sections.
        - Focus solely on the main content of the article.

        2. **Question Generation:**
        - Based on the main content, generate **2 fill in the blank questions** that cover the key topics and concepts discussed in the article.
        - **Do not** reference specifics such as locations, times, or use phrases like "in this study," "the authors," "this research," etc.
        - Ensure that questions are **self-contained** and **standalone**, meaning they do not require external context to be understood.
        - **Do not** generate questions other than fill in the blank questions. 

        3. **Answer Options:**
        - The answer should be open and clear. 

        **Text to generate questions and answers:  ```{text}```**

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

        - **Maintain Generality:** Questions should be applicable to the broader field or topic without referencing the source material.

        - **Clarity and Precision:** Ensure that questions and the answers are clear, precise, and free from ambiguity.

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

print(generate_FITB(article_data['Content'][0]))


question = ""
answer = ""

with open("FITB_dataset_test2.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Question", "Answer"])
    file.flush()

    for i in range(len(article_data['Content'])):

        article_text = article_data['Content'][i]

        generated_qa = generate_FITB(article_text)
        print(generated_qa)
        print("---------------------------------")

        split = generated_qa.split("\n")
        print(split)

        for j in split:
            if j.startswith("Question:"):
                question = j.replace("Question: ", "").strip()
            elif j.startswith("Answer:"):
                answer = j.replace("Answer: ", "").strip()

                writer.writerow([question, answer])
                file.flush()

            

