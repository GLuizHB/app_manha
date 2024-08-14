from flask import Flask, render_template,Request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novoaluno')
def cadastrar_aluno():
    return render_template('novoaluno.html')

@app.route('/logar',methods=['post'])
def logar_ra():
    ra = request.form['ra']
    return f"O RA informado é:{ra}"

@app.route('/diariobordo')
def diariobordo():
    return render_template('diariobordo.html')


app.run(debug=True)
