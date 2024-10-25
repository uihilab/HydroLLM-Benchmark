import openai
import pandas as pd
from secret import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

data = pd.read_csv("")

def check_qa(question, answer):
    prompt = f"""
    Your task is to perform the following actions.

    1. Read the Question and it's Answer: Review the question and it's answer within two triple backticks (```).
    2. Is the question and answer, check if they are numeric or not.
    3. Is the question location or article specific?
    3. If they are numeric, only return Yes, if not return No.

    Your only allowed response is Yes or No. Do return other responses other than Yes or No.

    Question and Answer to check: ```{question}``` ```{answer}``` 
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a question fixer. If there is a wrongly formatted question, you fix it."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=80
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

data['Valid'] = data.apply(lambda row: check_qa(data['Question'], data['Answers']), axis=1)

# Filter out the rows where 'Valid' is 'Yes' 
data_filtered = data[data['Valid'].str.lower() == 'no']

# Drop the 'Valid' column as it's no longer needed
data_filtered = data_filtered.drop(columns=['Valid'])

# Save the filtered DataFrame to a new CSV file
data_filtered.to_csv('mcq_article_postprocess_2.csv', index=False)

# Check for duplicate rows
#duplicates = df.duplicated()

# Count the number of duplicate rows
#num_duplicates = duplicates.sum()
#print(f'Number of duplicate rows: {num_duplicates}')

# If you want to remove duplicates
#df_no_duplicates = df.drop_duplicates()

#df_no_duplicates.to_csv(''.csv', index=False)
