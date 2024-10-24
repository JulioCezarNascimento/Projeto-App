from flask import Flask, request, jsonify

app = Flask(__name__)

# Dados simulados em memória
data = []

# Função para encontrar um item pelo ID
def find_item_by_id(item_id):
    return next((item for item in data if item['id'] == item_id), None)

# Endpoint para criar um novo item (Create)
@app.route('/items', methods=['POST'])
def create_item():
    item = request.get_json()
    if not item.get('id') or not item.get('name'):
        return jsonify({'error': 'ID e nome são obrigatórios'}), 400
    if find_item_by_id(item['id']):
        return jsonify({'error': 'ID já existe'}), 400
    data.append(item)
    return jsonify(item), 201

# Endpoint para listar todos os itens (Read)
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data)

# Endpoint para buscar um item específico pelo ID (Read)
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item_by_id(item_id)
    if item:
        return jsonify(item)
    return jsonify({'error': 'Item não encontrado'}), 404

# Endpoint para atualizar um item pelo ID (Update)
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({'error': 'Item não encontrado'}), 404
    updated_data = request.get_json()
    item.update(updated_data)
    return jsonify(item)

# Endpoint para deletar um item pelo ID (Delete)
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({'error': 'Item não encontrado'}), 404
    data.remove(item)
    return jsonify({'message': 'Item deletado com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)
