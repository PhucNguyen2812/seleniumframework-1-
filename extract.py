import pypdf
import sys

def convert_pdf(pdf_path, txt_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        with open(txt_path, 'w', encoding='utf-8') as f:
            for page in reader.pages:
                f.write(page.extract_text() + '\n')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    convert_pdf(sys.argv[1], sys.argv[2])
