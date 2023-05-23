from flask import Flask, render_template, request, url_for
import similarity


app = Flask(__name__, template_folder='Templates')

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route("/report")
def report():
    return render_template('/report.html')

@app.route("/members")
def members():
    return render_template('/members.html')

@app.route('/report', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form['text']
        report_data = similarity.report(str(result))
        html_table = similarity.returnTable(report_data)
        return render_template('report.html', table=html_table)

if __name__ == '__main__':
    app.run(debug=True)
