from PyPDF2 import PdfReader
import csv

pdf_path = input("Pdf path: ")

reader = PdfReader(pdf_path)

chapter_dict = {}
startings = []
endings = []

chapter_size = int(input("How many chapters are there? "))

for i in range(1,chapter_size+1):   
    chapter_start = int(input(f"Enter the first page of the chapter {i}: "))
    chapter_end = int(input(f"Enter the last page of the chapter {i}: "))
    startings.append(chapter_start-1)
    endings.append(chapter_end-1)

text = ""

for i in range(len(startings)):
    text = ""
    for page in range(startings[i], endings[i]):
        text += reader.pages[page].extract_text()
    chapter_dict[i] = text

output_path = input("Enter the output path, please include the file name and .csv extension: ")

try:
    with open(output_path, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ChapterID", "Text"])

        for chapter_id, text in chapter_dict.items():
            writer.writerow([chapter_id, text])
        print(f"CSV file has been successfully created and saved to {output_path}")
except Exception as e: 
    print(f"An error occured: {e}")