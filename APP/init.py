from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novoaluno')
def cadastrar_aluno():
    return render_template('novoaluno.html')

@app.route('/diariobordo')
def abrir_diario():
    return render_template('diariobordo.html')

@app.route('/logar',methods=['post'])
def logar_ra():
    ra = request.form['ra']
    if ra == "12345619":
        return render_template('diariobordo.html',ra=ra)
    else:
        mensagem = "RA INVALIDA"
        return render_template('index.html',mensagem=mensagem)




app.run(debug=True)
