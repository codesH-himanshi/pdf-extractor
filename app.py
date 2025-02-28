import os
from flask import Flask, request, render_template, send_file
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "pdf_file" not in request.files:
            return "No file part"
        
        pdf_file = request.files["pdf_file"]
        if pdf_file.filename == "":
            return "No selected file"
        
        pages = request.form.get("pages")
        if not pages:
            return "Please enter pages to extract"

        try:
            page_numbers = [int(p.strip()) - 1 for p in pages.split(",")]  # Convert to zero-based index
        except ValueError:
            return "Invalid page numbers format. Use comma-separated values (e.g., 1,3,5)."

        input_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "extracted_" + pdf_file.filename)

        pdf_file.save(input_path)
        extract_pages(input_path, output_path, page_numbers)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

def extract_pages(input_pdf, output_pdf, pages_to_extract):
    with open(input_pdf, "rb") as infile:
        reader = PyPDF2.PdfReader(infile)
        writer = PyPDF2.PdfWriter()
        
        for page_num in pages_to_extract:
            if 0 <= page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
        
        with open(output_pdf, "wb") as outfile:
            writer.write(outfile)

if __name__ == "__main__":
    app.run(debug=True)
