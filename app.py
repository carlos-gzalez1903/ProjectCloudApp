from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        description = request.form['description']
        new_task = {
            'id': len(tasks) + 1,
            'description': description,
            'date_added': datetime.now().strftime('%Y-%m-%d'),
            'date_resolved': None,
            'status': 'Pendiente'
        }
        tasks.append(new_task)
        return redirect(url_for('index'))
    return render_template('task_form.html')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'Completada'
            task['date_resolved'] = datetime.now().strftime('%Y-%m-%d')
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)