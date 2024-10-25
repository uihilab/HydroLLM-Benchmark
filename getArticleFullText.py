import requests
import os
import csv
import time
import re
import logging
from secret import ELSEVIER_API_KEY  # Ensure this file exists with the correct API key

def fetch_article_content(doi, api_key, view=None, accept='text/plain'):
    """
    Fetch the full-text or abstract of an article using its DOI.

    Parameters:
    - doi (str): The DOI of the article.
    - api_key (str): Your Elsevier API key.
    - view (str): 'FULL' to request full-text view, None for default.
    - accept (str): The desired response format ('text/xml' or 'text/plain').

    Returns:
    - dict: A dictionary with 'DOI', 'Status', 'Content', and 'Error' (if any).
    """
    # Base URL
    base_url = f"https://api.elsevier.com/content/article/doi/{doi}"
    
    # Headers
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': accept
    }
    
    # Parameters
    params = {}
    if view:
        params['view'] = view  # 'FULL' or 'META_ABS'
    
    try:
        # Make the GET request
        response = requests.get(base_url, headers=headers, params=params)
        
        # Check response status
        if response.status_code == 200:
            # Successful retrieval
            content = response.text
            return {
                'DOI': doi,
                'Status': 'Success',
                'Content': content,
                'Error': None
            }
        elif response.status_code == 401:
            # Unauthorized
            return {
                'DOI': doi,
                'Status': 'Error',
                'Content': None,
                'Error': 'Authorization Error: Check your API key and permissions.'
            }
        elif response.status_code == 404:
            # Not Found
            return {
                'DOI': doi,
                'Status': 'Error',
                'Content': None,
                'Error': 'Article not found.'
            }
        elif response.status_code == 403:
            # Forbidden - likely not entitled for full-text
            return {
                'DOI': doi,
                'Status': 'Not Entitled',
                'Content': None,
                'Error': 'Not entitled to access full-text. Only abstract available.'
            }
        else:
            # Other errors
            return {
                'DOI': doi,
                'Status': 'Error',
                'Content': None,
                'Error': f'HTTP Error: {response.status_code}'
            }
    except Exception as e:
        # Handle exceptions
        return {
            'DOI': doi,
            'Status': 'Error',
            'Content': None,
            'Error': str(e)
        }

def clean_content(content):
    """
    Removes all HTTP and HTTPS URLs from the content.

    Parameters:
    - content (str): The text content to clean.

    Returns:
    - str: The cleaned content without URLs.
    """
    # Regex pattern to match URLs
    url_pattern = r'http[s]?://\S+'
    # Substitute URLs with an empty string
    cleaned = re.sub(url_pattern, '', content)
    # Optionally, you can replace URLs with a placeholder like [URL]
    # cleaned = re.sub(url_pattern, '[URL]', content)
    return cleaned

def main():
    # Configure logging
    logging.basicConfig(
        filename='retrieve_full_text.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    
    # Retrieve API key from secret.py
    api_key = ELSEVIER_API_KEY
    if not api_key:
        logging.error("API key not found. Please set the ELSEVIER_API_KEY in secret.py.")
        print("Error: API key not found. Please set the ELSEVIER_API_KEY in secret.py.")
        return
    
    # Input CSV containing DOIs and optionally Titles
    input_csv = ''  # Replace with your CSV file path
    
    # Output CSV to store titles and contents
    output_csv = ''  # Replace with desired output path
    
    # Open the output CSV in write mode and set up the writer with headers
    try:
        with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
            fieldnames = ['Title', 'Content']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Read DOIs from input CSV
            try:
                with open(input_csv, 'r', encoding='utf-8') as infile:
                    reader = csv.DictReader(infile)
                    
                    # Check if 'DOI' column exists
                    if 'DOI' not in reader.fieldnames:
                        logging.error("Input CSV must contain a 'DOI' column.")
                        print("Error: Input CSV must contain a 'DOI' column.")
                        return
                    
                    # Determine if 'Title' column exists
                    has_title = 'Title' in reader.fieldnames
                    
                    for row in reader:
                        doi = row.get('DOI', '').strip()
                        title = row.get('Title', 'N/A').strip() if has_title else 'N/A'
                        
                        if not doi:
                            logging.warning(f"Skipping row with missing DOI. Title: {title}")
                            print(f"Skipping row with missing DOI. Title: {title}")
                            continue
                        
                        logging.info(f"Fetching content for DOI: {doi}")
                        print(f"Fetching content for DOI: {doi}")
                        
                        # Attempt to fetch full-text
                        result = fetch_article_content(doi, api_key, view='FULL', accept='text/plain')
                        if result['Status'] == 'Success':
                            # Full-text retrieved
                            content = result['Content']
                            logging.info(f"Full-text retrieved for DOI: {doi}")
                            print(f"Full-text retrieved for DOI: {doi}")
                        elif result['Status'] == 'Not Entitled':
                            # Only abstract available, attempt to fetch abstract
                            logging.info(f"Not entitled to full-text for DOI: {doi}. Attempting to fetch abstract.")
                            print(f"Not entitled to full-text for DOI: {doi}. Attempting to fetch abstract.")
                            # Fetch abstract without 'view=FULL'
                            abstract_result = fetch_article_content(doi, api_key, view=None, accept='text/plain')
                            if abstract_result['Status'] == 'Success':
                                # Abstract retrieved
                                content = abstract_result['Content']
                                logging.info(f"Abstract retrieved for DOI: {doi}")
                                print(f"Abstract retrieved for DOI: {doi}")
                                # Update result status
                                result = {
                                    'DOI': doi,
                                    'Status': 'Abstract Retrieved',
                                    'Content': content,
                                    'Error': None
                                }
                            else:
                                # Failed to retrieve abstract
                                logging.error(f"Failed to retrieve abstract for DOI: {doi}. Error: {abstract_result['Error']}")
                                print(f"Failed to retrieve abstract for DOI: {doi}. Error: {abstract_result['Error']}")
                                content = ''
                                # Update result
                                result = abstract_result
                        else:
                            # Other errors
                            logging.error(f"Error fetching content for DOI: {doi}. Error: {result['Error']}")
                            print(f"Error fetching content for DOI: {doi}. Error: {result['Error']}")
                            content = ''
                        
                        # Decide whether to save the content
                        save_entry = True  # Set to False to skip saving
                        
                        # **Optional User Confirmation**
                        # Uncomment the following lines to prompt the user for each entry
                        '''
                        user_input = input(f"Do you want to save the content for '{title}'? (y/n): ").strip().lower()
                        if user_input != 'y':
                            save_entry = False
                        '''
                        
                        if result['Status'] == 'Success' or result['Status'] == 'Abstract Retrieved':
                            # Clean the content by removing URLs
                            cleaned_content = clean_content(content)
                            # Optionally, replace multiple spaces with a single space
                            cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
                            
                            if save_entry:
                                writer.writerow({
                                    'Title': title,
                                    'Content': cleaned_content
                                })
                                logging.info(f"Saved content for DOI: {doi}")
                                print(f"Saved content for DOI: {doi}")
                        else:
                            # Handle errors by logging and optionally writing to CSV
                            error_message = f"Error: {result['Error']}" if result['Error'] else 'N/A'
                            if save_entry:
                                writer.writerow({
                                    'Title': title,
                                    'Content': error_message
                                })
                                logging.info(f"Saved error for DOI: {doi}")
                                print(f"Saved error for DOI: {doi}")
                        
                        # Append a small delay to respect rate limits
                        time.sleep(1)
            except FileNotFoundError:
                logging.error(f"Input CSV file '{input_csv}' not found.")
                print(f"Error: Input CSV file '{input_csv}' not found.")
                return
    except Exception as e:
        logging.error(f"Failed to open output CSV file '{output_csv}'. Error: {str(e)}")
        print(f"Error: Failed to open output CSV file '{output_csv}'. Error: {str(e)}")
        return
    
    print(f"Titles and contents have been saved to {output_csv}")
    logging.info(f"Titles and contents have been saved to {output_csv}")

if __name__ == "__main__":
    main()