import pdfplumber

def extract_columns(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf, open(output_path, "w", encoding="utf-8") as f_out:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_width = page.width
            page_height = page.height

            # Define column boundaries (adjust as needed)
            # Example: Two equal-width columns
            left_bbox = (0, 0, page_width / 2 - 10, page_height)   # Subtract 10 for a margin
            right_bbox = (page_width / 2 + 10, 0, page_width, page_height)  # Add 10 for a margin

            # Extract text from left column
            left_text = page.within_bbox(left_bbox).extract_text()
            if left_text:
                #f_out.write(f"--- Page {page_number} - Left Column ---\n")
                f_out.write(left_text + "\n\n")

            # Extract text from right column
            right_text = page.within_bbox(right_bbox).extract_text()
            if right_text:
                #f_out.write(f"--- Page {page_number} - Right Column ---\n")
                f_out.write(right_text + "\n\n")

            f_out.write("\n")  # Add space between pages

    print(f"Text extraction complete. Output saved to '{output_path}'.")

if __name__ == "__main__":
    pdf_path = ""    
    output_path = "output.txt"  
    extract_columns(pdf_path, output_path)