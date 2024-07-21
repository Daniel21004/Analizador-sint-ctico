from flask import Flask, request, render_template
from automata import evaluar

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = ""
    if request.method == 'POST':
        input_text = request.form['input_text']
        lineas = input_text.splitlines()
        resultados = evaluar(lineas)
        print(resultados)
    return render_template('index.html', resultados=resultados)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
