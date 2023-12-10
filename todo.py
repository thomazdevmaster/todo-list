from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = {}
id = 0

def generate_unique_id():
    global id
    id += 1
    return id 

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id_task =  generate_unique_id()
    task = {
        'id': id_task,
        'description': data.get('description'),
        'status': 'pending',
        'created_at': current_time,
        'updated_at': None,
        'completed_at': None
    }
    tasks[id_task] = task
    return jsonify({'message': 'Tarefa adicionada cokm sucesso', "id": id_task})



@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    if task_id in tasks:
        return jsonify({'task': tasks[task_id]})
    else:
        return jsonify({'error': 'Tarefa não existe'}), 404



@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id in tasks:
        data = request.get_json()

        data['id'] = tasks[task_id]['id']
        data['created_at'] = tasks[task_id]['created_at']

        tasks[task_id]['description'] = data.get('description')

        tasks[task_id]['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return jsonify({'message': 'Tarefa atualizada com sucesso'})
    else:
        return jsonify({'error': 'Tarefa não existe'}), 404
    
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({'message': 'Tarefa apagada com sucesso'})
    else:
        return jsonify({'error': 'Tarefa não existe'}), 404

if __name__ == '__main__':
    app.run(debug=True)