from datetime import datetime
import json
import os
import base64
from flask import Flask, jsonify, request

app = Flask(__name__)

tasks_file_path = 'tasks.json'


def generate_unique_id():
    max_id = max(tasks.keys(), default=0)
    return str(int(max_id) + 1)


def load_tasks_from_file():
    if os.path.exists(tasks_file_path):
        with open(tasks_file_path, 'r') as file:
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError:
                return {}
    else:
        return {}
        

def save_tasks(tasks_data):
    with open(tasks_file_path, 'w') as file:
        json.dump(tasks_data, file, indent=2)

tasks = load_tasks_from_file()

@app.route('/', methods=['GET'])
def home():
    user_name = os.environ.get('USER_NAME', 'usuário')
    secret_value = os.environ.get('SECRET_VALUE', 'TsOjbyBmb2kgaW5mb3JtYWRv')

    decoded_bytes = base64.b64decode(secret_value)
    decoded_string = decoded_bytes.decode('utf-8')

    return jsonify({"message": f"Olá {user_name}, essa é sua api de tarefas, exemplo de secrets em base64 é {secret_value} e decodificado é ({decoded_string})"})


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
    save_tasks(tasks)
    return jsonify({'message': 'Tarefa adicionada com sucesso', "id": id_task}), 201



@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    if task_id in tasks:
        return jsonify({'task': tasks[task_id]}), 200
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

        save_tasks(tasks)
        return jsonify({'message': 'Tarefa atualizada com sucesso'}), 200
    else:
        return jsonify({'error': 'Tarefa não existe'}), 404
    
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        save_tasks(tasks)
        return jsonify({'message': 'Tarefa apagada com sucesso'})
    else:
        return jsonify({'error': 'Tarefa não existe'}), 404

if __name__ == '__main__':
    app.run(debug=True)