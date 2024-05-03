from flask import Flask, jsonify, request, render_template, url_for
import pyodbc

app = Flask(__name__)

driver = 'ODBC Driver 17 for SQL Server'
server = 'localhost'
database = 'db_ControleEstoque1'
username = 'devGustavo'
password = '1234'   

@app.route('/')
def index():
    global conn, cursor
    conn = pyodbc.connect(f'DRIVER={{{driver}}};'
                      f'SERVER={server};'
                      f'DATABASE={database};'
                      f'UID={username};'
                      f'PWD={password}'
                      )

    cursor = conn.cursor()
    return render_template('index.html')



@app.route('/usuarios', methods=['GET'])
def obter_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    
    usuarios_list = [
        {
            'id': row[0],
            'nome': row[1],
            'cpf': row[2],
            'dataNascimento': row[3]
        } for row in usuarios
    ]
    
    return jsonify(usuarios_list)

@app.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario_por_id(id):
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", id)
    usuario = cursor.fetchone()
    
    if usuario:
        return jsonify({
            'id': usuario[0],
            'nome': usuario[1],
            'cpf': usuario[2],
            'dataNascimento': usuario[3]
        })
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuario_por_id(id):
    usuario_alterado = request.get_json()
    cursor.execute("UPDATE usuarios SET id = ?, nome = ?, cpf = ?, dataNascimento = ? WHERE id = ?", 
                   usuario_alterado['nome'], usuario_alterado['cpf'], usuario_alterado['dataNascimento'], id)
    conn.commit()
    
    return jsonify({'message': 'Usuário atualizado com sucesso'})

@app.route('/usuarios', methods=['POST'])
def incluir_novo_usuario():
    novo_usuario = request.get_json()
    cursor.execute("INSERT INTO usuarios (id, nome, cpf, dataNascimento) VALUES (?, ?, ?, ?)",
                   novo_usuario['id'], novo_usuario['nome'], novo_usuario['cpf'], novo_usuario['dataNascimento'])
    conn.commit()
    
    return jsonify({'message': 'Novo usuário criado com sucesso'})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    cursor.execute("DELETE FROM usuarios WHERE id = ?", id)
    conn.commit()
    
    return jsonify({'message': 'Usuário excluído com sucesso'})

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)