import requests
import json
import time
import csv
import os
from secret import ELSEVIER_API_KEY

# -----------------------------
# Configuration
# -----------------------------

# List of target journals
journals = [
    "Journal of Hydrology",
    "Advances in Water Resources",
    "Journal of Hydrology: Regional Studies"
]

# Publication years from 2022 to 2024
start_year = 2022
end_year = 2024

# Base URL for the Scopus Search API
base_url = "https://api.elsevier.com/content/search/scopus"

api_key = ELSEVIER_API_KEY

if not api_key:
    raise ValueError("API key not found. Please set the ELSEVIER_API_KEY environment variable.")

# Number of records to retrieve per request
count = 25  # Adjust based on API documentation; common values are 25, 50, 100

# Initialize start index
start = 0

# Initialize a list to store all articles
all_articles = []

# Flag to control the loop
more_records = True

# -----------------------------
# Construct the Query
# -----------------------------

# Constructing the query for journals
# SRCTITLE searches for the exact journal title
journal_queries = ' OR '.join([f'SRCTITLE("{journal}")' for journal in journals])

# Constructing the query for publication years
# PUBYEAR > 2021 AND PUBYEAR < 2025 filters for 2022-2024
year_query = f'PUBYEAR > {start_year - 1} AND PUBYEAR < {end_year + 1}'

# Combined query
full_query = f'({journal_queries}) AND ({year_query})'

print(f"Constructed Query: {full_query}")

# -----------------------------
# Fetch Data with Pagination
# -----------------------------

while more_records:
    # Define query parameters
    params = {
        'query': full_query,
        'apiKey': api_key,
        'start': start,
        'count': count,
        'view': 'STANDARD',  # Use 'STANDARD' to include basic fields
        'field': 'dc:title,prism:coverDate,prism:publicationName,prism:doi'  # Specify desired fields
    }

    try:
        # Make the GET request
        response = requests.get(base_url, params=params)
        
        # Raise an HTTPError if the response was unsuccessful
        response.raise_for_status()
        
        data = response.json()
        
        # Extract the entries
        entries = data.get('search-results', {}).get('entry', [])
        
        if not entries:
            print("No more records found.")
            break
        
        # Append entries to the all_articles list
        all_articles.extend(entries)
        
        # Update the start index for the next batch
        start += count
        
        # Check if we've retrieved all records
        total_results = int(data.get('search-results', {}).get('opensearch:totalResults', 0))
        print(f"Retrieved {len(all_articles)} of {total_results} records.")
        
        if len(all_articles) >= total_results:
            more_records = False
        else:
            # To respect rate limits, pause between requests
            time.sleep(1)  # Adjust as per API rate limits
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Authorization Error: Check your API key and permissions.")
            print(f"Response: {response.text}")
            break
        elif response.status_code == 429:
            # Handle rate limit exceeded
            print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
            time.sleep(60)
            continue
        else:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response: {response.text}")
            break
    except Exception as err:
        print(f"An error occurred: {err}")
        break

# -----------------------------
# Extract Relevant Data
# -----------------------------

if all_articles:
    extracted_data = []
    
    for entry in all_articles:
        # Extract Title
        title = entry.get('dc:title', 'N/A')
        
        # Extract Publication Year
        cover_date = entry.get('prism:coverDate', 'N/A')
        publication_year = cover_date[:4] if cover_date != 'N/A' else 'N/A'  # Extract year from date
        
        # Extract Journal Name using 'prism:publicationName'
        journal_name = entry.get('prism:publicationName', 'N/A')
        
        # Extract DOI
        doi = entry.get('prism:doi', 'N/A')
        
        # Append to extracted_data
        extracted_data.append({
            'Title': title,
            'Publication Year': publication_year,
            'Journal Name': journal_name,
            'DOI': doi
        })
    
    print(f"Extracted {len(extracted_data)} articles.")
    
    # -----------------------------
    # Save Data to JSON
    # -----------------------------
    
    with open('elsevier_articles.json', 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)
    
    print("Data has been saved to elsevier_articles.json")
    
    # -----------------------------
    # Save Data to CSV (Optional)
    # -----------------------------
    
    # Define CSV file headers
    headers = ['Title', 'Publication Year', 'Journal Name', 'DOI']
    
    # Save to CSV
    with open('elsevier_articles.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for article in extracted_data:
            writer.writerow(article)
    
    print("Data has been saved to elsevier_articles.csv")
else:
    print("No articles were retrieved.")