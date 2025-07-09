
import os                                                                # Importing os for file operations 
import re                                                                # Importing os for file operations and re for regular expressions
from pathlib import Path                                                 # Importing Path from pathlib to handle file paths
from PyPDF2 import PdfMerger,PdfReader                                   # Importing PdfMerger from PyPDF2 to handle PDF merging


current_path_os = os.getcwd()                                           # Get the current working directory using os.getcwd()   
print(f"Current path (using os.getcwd()): {current_path_os}")

# This script merges multiple PDF files in a specified folder into a single PDF file. In this script, we use the PyPDF2 library to handle PDF merging.
# Make sure to install PyPDF2 using pip if you haven't already: # pip install PyPDF2 

def merge_pdfs_with_skipping_first_page(input_folder, output_file):
    """
    Merges all PDFs in the input_folder into a single output PDF file.

    Args:
        input_folder (str): Path to the folder containing PDFs to merge.
        output_file (str): Name of the output merged PDF file.
    """
    pdf_merger = PdfMerger()

    # Get all PDF files in the input folder
    pdf_files = [file for file in os.listdir(input_folder) if file.lower().endswith('.pdf')]
    print(f"The total file length: {len(pdf_files)}")
    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return

    def sort_key(filename):
        # Extract week number (e.g., "1" from "Week1...") and suffix (e.g., "(2)" → 2, default 0)
        week_num = int(re.search(r"Week(\d+)", filename).group(1))
        suffix_match = re.search(r"\((\d+)\)\.pdf$", filename)
        suffix = int(suffix_match.group(1)) if suffix_match else 0
        return (week_num, suffix)  # Sort by week first, then suffix
    
    # Sort the PDF files based on the week number
    pdf_files.sort(key=sort_key)
    for Pdf in pdf_files:
        print(Pdf)

    try:
        for pdf_file in pdf_files:
            file_path = os.path.join(input_folder, pdf_file)
            with open(file_path, 'rb') as f:
                pdf_reader = PdfReader(f)
                if len(pdf_reader.pages) > 1:
                    # Add all the pages except the first page (index starts at 0)       
                    pdf_merger.append(file_path, pages=(1, len(pdf_reader.pages)))
                else:
                    print(f"skipping {pdf_file} (only one page).")
        
        # Write the merged PDF to the output file
        pdf_merger.write(output_file)
        print(f"Successfully merged {len(pdf_files)} PDFs into {output_file} excluding first pages.")
    
    except Exception as e:
        print(f"Error merging PDFs: {e}")
    finally:
        pdf_merger.close()    

if __name__ == "__main__":
    input_folder = input("Enter the folder path containing PDFs: ").strip()
    output_file = input("Enter the output merged PDF filename (e.g., merged.pdf): ").strip()
    
    merge_pdfs_with_skipping_first_page(input_folder, output_file)