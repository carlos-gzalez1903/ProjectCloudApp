from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# Base de datos temporal para las tareas
tasks = [
    {
        'id': 1,
        'description': 'Aprender Flask',
        'date_added': '2023-05-15',
        'date_resolved': None,
        'status': 'Pendiente'
    },
    {
        'id': 2,
        'description': 'Crear API REST',
        'date_added': '2023-05-16',
        'date_resolved': '2023-05-18',
        'status': 'Completada'
    }
]
@app.route('/api/tasks', methods=['GET', 'POST'])  
def handle_tasks():
    if request.method == 'GET':
        return jsonify({"tasks": tasks})  
    elif request.method == 'POST':
        # Lógica para crear tarea
        return jsonify({"message": "Tarea creada"}), 201

# GET /api/tasks/<id>
@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((t for t in tasks if t['id'] == id), None)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(task)

# POST /api/tasks
@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'description' not in request.json:
        return jsonify({"error": "Descripción requerida"}), 400
    
    new_task = {
        "id": len(tasks) + 1,
        "description": request.json['description'],
        "status": "pending",
        "created_at": datetime.now().strftime('%Y-%m-%d')
    }
    tasks.append(new_task)
    return jsonify({"message": "Tarea creada", "id": new_task['id']}), 201

# PUT /api/tasks/<id>
@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = next((t for t in tasks if t['id'] == id), None)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    task['description'] = request.json.get('description', task['description'])
    task['status'] = request.json.get('status', task['status'])
    return jsonify({"message": f"Tarea {id} actualizada"})

# DELETE /api/tasks/<id>
@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t['id'] != id]
    return jsonify({"message": f"Tarea {id} eliminada"})


if __name__ == '__main__':
    app.run(debug=True)