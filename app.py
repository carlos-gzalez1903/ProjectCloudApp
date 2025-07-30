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

# Ruta principal que renderiza la interfaz web
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

# Ruta para agregar tareas desde el formulario web
@app.route('/add', methods=['POST'])
def add_task():
    description = request.form.get('description')
    if not description:
        return redirect(url_for('index'))
    
    new_task = {
        'id': len(tasks) + 1,
        'description': description,
        'date_added': datetime.now().strftime('%Y-%m-%d'),
        'date_resolved': None,
        'status': 'Pendiente'
    }
    tasks.append(new_task)
    return redirect(url_for('index'))

# Ruta para marcar tarea como completada
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'Completada'
            task['date_resolved'] = datetime.now().strftime('%Y-%m-%d')
            break
    return redirect(url_for('index'))

# API REST
@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify({"tasks": tasks})

@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((t for t in tasks if t['id'] == id), None)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(task)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'description' not in request.json:
        return jsonify({"error": "Descripción requerida"}), 400
    
    new_task = {
        "id": len(tasks) + 1,
        "description": request.json['description'],
        "status": "Pendiente",
        "date_added": datetime.now().strftime('%Y-%m-%d'),
        "date_resolved": None
    }
    tasks.append(new_task)
    return jsonify({"message": "Tarea creada", "task": new_task}), 201

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = next((t for t in tasks if t['id'] == id), None)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    data = request.json
    task['description'] = data.get('description', task['description'])
    task['status'] = data.get('status', task['status'])
    if task['status'] == 'Completada' and not task['date_resolved']:
        task['date_resolved'] = datetime.now().strftime('%Y-%m-%d')
    return jsonify({"message": f"Tarea {id} actualizada", "task": task})

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t['id'] != id]
    return jsonify({"message": f"Tarea {id} eliminada"})

if __name__ == '__main__':
    app.run(debug=True)