from flask import Flask, request, jsonify

app = Flask(__name__)

livros = []
contador_id = 1

# 📌 ROTA GET - listar todos os livros
@app.route('/livros', methods=['GET'])
def listar_livros():
    return jsonify(livros), 200


# 📌 ROTA GET - buscar livro por ID
@app.route('/livros/<int:id>', methods=['GET'])
def buscar_livro(id):
    for livro in livros:
        if livro['id'] == id:
            return jsonify(livro), 200
    return {"erro": "Livro não encontrado"}, 404


# 📌 ROTA POST - cadastrar livro
@app.route('/livros', methods=['POST'])
def cadastrar_livro():
    global contador_id

    dados = request.json

    # ✅ Validação de dados obrigatórios
    if not dados.get('titulo') or not dados.get('autor'):
        return {"erro": "Título e autor são obrigatórios"}, 400

    # ✅ Validação de ano
    if dados.get('ano') is None or dados['ano'] < 0:
        return {"erro": "Ano inválido"}, 400

    # ✅ Evitar duplicados
    for l in livros:
        if l['titulo'].lower() == dados['titulo'].lower():
            return {"erro": "Livro já cadastrado"}, 400

    novo_livro = {
        "id": contador_id,
        "titulo": dados['titulo'],
        "autor": dados['autor'],
        "ano": dados['ano']
    }

    livros.append(novo_livro)
    contador_id += 1

    return {
        "mensagem": "Livro cadastrado com sucesso",
        "livro": novo_livro
    }, 201


# 📌 ROTA PUT - atualizar livro
@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    dados = request.json

    for livro in livros:
        if livro['id'] == id:

            if dados.get('titulo'):
                livro['titulo'] = dados['titulo']

            if dados.get('autor'):
                livro['autor'] = dados['autor']

            if dados.get('ano') is not None:
                if dados['ano'] < 0:
                    return {"erro": "Ano inválido"}, 400
                livro['ano'] = dados['ano']

            return {
                "mensagem": "Livro atualizado com sucesso",
                "livro": livro
            }, 200

    return {"erro": "Livro não encontrado"}, 404


# 📌 ROTA DELETE - excluir livro
@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    for livro in livros:
        if livro['id'] == id:
            livros.remove(livro)
            return {"mensagem": "Livro excluído com sucesso"}, 200

    return {"erro": "Livro não encontrado"}, 404


if __name__ == '__main__':
    app.run(debug=True)