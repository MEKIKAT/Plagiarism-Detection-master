from flask import Flask, render_template, request
import os
from docx import Document
import string

app = Flask(__name__)

local_archive_directory = 'local_archive'

def detect_plagiarism(submitted_text):
    plagiarism_report = ""
    submitted_text = submitted_text.translate(str.maketrans('', '', string.punctuation)).lower()

    for filename in os.listdir(local_archive_directory):
        file_path = os.path.join(local_archive_directory, filename)

        if not os.path.isfile(file_path):
            continue

        doc = Document(file_path)
        document_text = ""
        for paragraph in doc.paragraphs:
            document_text += paragraph.text + "\n"
        document_text = document_text.translate(str.maketrans('', '', string.punctuation)).lower()

        similarity = calculate_similarity(submitted_text, document_text)
        if similarity > 0.8:
            plagiarism_report += f"Similarity: {similarity}\nDocument: {filename}\n\n"

    if not plagiarism_report:
        plagiarism_report = "No plagiarism detected."

    return plagiarism_report

def calculate_similarity(text1, text2):

    words1 = set(text1.split())
    words2 = set(text2.split())
    common_words = words1.intersection(words2)
    similarity = len(common_words) / len(words1)
    return similarity

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect-plagiarism', methods=['POST'])
def detect():
    text = request.form['text']
    plagiarism_report = detect_plagiarism(text)
    return render_template('index.html', report=plagiarism_report)

if __name__ == '__main__':
    app.run(debug=True)
