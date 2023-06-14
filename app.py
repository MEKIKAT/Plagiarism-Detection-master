from flask import Flask, render_template, request
import os
from docx import Document
import string

app = Flask(__name__)

local_archive_directory = 'local_archive'
k = 3 # Value of k for k-gram similarity

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
    k_grams1 = generate_k_grams(text1)
    k_grams2 = generate_k_grams(text2)

    common_k_grams = k_grams1.intersection(k_grams2)
    similarity = len(common_k_grams) / len(k_grams1)
    return similarity

def generate_k_grams(text):
    k_grams = set()

    for i in range(len(text) - k + 1):
        k_gram = text[i:i+k]
        k_grams.add(k_gram)

    return k_grams

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
