from PyPDF2 import PdfReader, PdfWriter


def extract_page_range(input_path, output_path, start_page, end_page):
    try:
        # Create PDF reader object
        reader = PdfReader(input_path)

        # Create PDF writer object
        writer = PdfWriter()

        # Add pages from start_page to end_page (converting to 0-based indexing)
        for page_num in range(start_page - 1, end_page):
            if page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])

        # Write the output PDF
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        print(f"Successfully created PDF with pages {start_page} to {end_page}")

    except Exception as e:
        print(f"Error: {str(e)}")


# Usage
input_file = "AI_Russell_Norvig.pdf"
output_file = "ai_extracted_pages.pdf"
start = 94
end = 110

extract_page_range(input_file, output_file, start, end)
