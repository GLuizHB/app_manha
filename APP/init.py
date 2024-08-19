from flask import Flask,render_template,request,redirect,url_for,flash

from flask_sqlalchemy import SQLAlchemy

# Importa a função `sessionmaker`, que é usada para criar uma nova sessão para interagir com o banco de dados
from sqlalchemy.orm import sessionmaker

# Importa as funções `create_engine` para estabelecer uma conexão com o banco de dados e `MetaData` para trabalhar com metadados do banco de dados
from sqlalchemy import create_engine, MetaData

# Importa a função `automap_base`, que é usada para refletir um banco de dados existente em classes ORM automaticamente
from sqlalchemy.ext.automap import automap_base
from aluno import Aluno

"""
O MetaData no SQLAlchemy é uma classe que representa a coleção de esquemas de tabelas, 
incluindo informações como tabelas, colunas, chaves, índices e outros elementos associados
a um banco de dados.

"""

"""
Criando nossa aplicação

app é um objeto
Flask( ) é um construtor
__name__ é o nome da aplicação
"""
app = Flask(__name__)

# Criando a configuração do banco de dados
# Configuração do Banco de Dados
# biblioteca para converter e resolver problema do @
import urllib.parse

# Qual o usuário do banco e a senha?

user = 'root'
password = urllib.parse.quote_plus('senai@123')

host = 'localhost'
database = 'projetodiario1'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# Criar a engine e refletir o banco de dados existente
engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

# Mapeamento automático das tabelas para classes Python
Base = automap_base(metadata=metadata)
Base.prepare()

# Acessando a tabela 'aluno' mapeada
Aluno = Base.classes.aluno

# Criar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastro')
def cadastrar_aluno():
    return render_template('novoaluno.html')

@app.route('/diario')
def abirdiario():
    return render_template('dirariobordo.html')

@app.route('/logar', methods=['POST'])
def logar():
    ra = request.form['ra']
    aluno = session.query(Aluno).filter_by(ra=ra).first()
    
    if aluno:
        nome = aluno.nome  # Extrai o nome do aluno
        return render_template('diariobordo.html', ra=ra, nome=nome)
    else:
        mensagem = "RA INVALIDA"
        return render_template('index.html', mensagem=mensagem)


@app.route('/criaraluno', methods=['POST'])
def criar():
    ra = request.form['ra']
    nome = request.form['nome']
    tempoestudo = int(request.form['tempoestudo'])
    rendafamiliar = float(request.form['rendafamiliar'])

    aluno_existente = session.query(Aluno).filter_by(ra=ra).first()

    if aluno_existente:
        mensagem = "RA já cadastrado no sistema."
        return render_template('index.html', msgbanco=mensagem)

    aluno = Aluno(ra=ra,nome=nome,tempoestudo=tempoestudo,rendafamiliar=rendafamiliar)
    
    try:
        session.add(aluno) #  Adiciona um novo objeto aluno à sessão para ser inserido no banco de dados.
        session.commit() # Confirma a transação, salvando as mudanças no banco de dados.
    except:
        session.rollback() # Desfaz qualquer mudança feita na sessão durante a transação, revertendo o banco de dados ao estado anterior.
        raise # Relevanta a exceção original, permitindo que seja tratada em outro nível do código ou exibida como um erro
    finally:
        session.close() # Fecha a sessão, garantindo que os recursos sejam liberados, independentemente de a transação ter sido bem-sucedida ou não.

    return redirect(url_for('listar_alunos'))



@app.route('/alunos', methods=['GET'])
def listar_alunos():
    try:
        # Busca todos os alunos cadastrados no banco de dados
        alunos = session.query(Aluno).all()
    except:
        session.rollback()
        mensagem = "Erro ao tentar recuperar a lista de alunos."
        return render_template('index.html', msgbanco=mensagem)
    finally:
        session.close()

    # Renderiza o template HTML passando a lista de alunos
    return render_template('listar_alunos.html', alunos=alunos)









app.run(debug=True)