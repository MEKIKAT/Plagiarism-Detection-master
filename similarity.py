import nltk
import websearch
from difflib import SequenceMatcher
import pandas as pd

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(nltk.corpus.stopwords.words('english'))


def purifyText(string):
    words = nltk.word_tokenize(string)
    return " ".join([word for word in words if word not in stop_words])


def webVerify(string, results_per_sentence):
    sentences = nltk.sent_tokenize(string)
    matching_sites = []

    for url in websearch.searchBing(query=string, num=results_per_sentence):
        matching_sites.append(url)

    for sentence in sentences:
        for url in websearch.searchBing(query=sentence, num=results_per_sentence):
            matching_sites.append(url)

    return list(set(matching_sites))


def similarity(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio() * 100


def report(text):
    matching_sites = webVerify(purifyText(text), 2)
    matches = {}

    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = similarity(text, websearch.extractText(matching_sites[i]))

    matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}

    return matches



def returnTable(dictionary):
    df = pd.DataFrame({"Matching Site": dictionary.keys(), "Similarity (%)": dictionary.values()})
    df["Visit site"] = df["Matching Site"].apply(lambda x: f'<button onclick="window.open(\'{x}\', \'_blank\')" style="background-color: #e67e22; color: #ecf0f1; border: 1px solid #f39c12; border-radius: 5px; padding: 10px; cursor: pointer;">Open Link</button>')

    html_table = '<table style="width: 100%; border-collapse: collapse; border: solid #000 1px;">'
    html_table += '<tr style="background: #7CAE00; color: white; font-family: verdana; border: solid #000 1px; ">'
    html_table += '<th style="padding: 10px; border: solid #000 1px; ">Matching Site</th>'
    html_table += '<th style="padding: 10px; border: solid #000 1px;">Similarity (%)</th>'
    html_table += '<th style="padding: 10px; border: solid #000 1px;">Visit site</th>'
    html_table += '</tr>'

    for _, row in df.head(20).iterrows():
        html_table += '<tr style="background: #DCDCDC;">'
        html_table += f'<td style="padding: 10px; max-width: 2.5cm; word-wrap: break-word;">{row["Matching Site"]}</td>'
        html_table += f'<td style="padding: 10px;">{row["Similarity (%)"]}</td>'
        html_table += f'<td style="padding: 10px;">{row["Visit site"]}</td>'
        html_table += '</tr>'

    html_table += '</table>'
    
    return html_table






if __name__ == "__main__":
    report("This is a pure test")
