from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URl']='mysql://username:password@localhost/db_name'  # Replace with your MySQL database URL
db = SQLAlchemy(app)

class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    description=db.Column(db.String(255))
    due_date=db.Column(db.Date)
    completed=db.Column(db.Boolean,default=False)
    date_completed=db.Column(db.Date)

@app.route('/tasks', methods=['POST'])
def create_task():
    data=request.get_json()
    task=Task(name=data['name'],description=data.get('description'),due_date=data.get('due_date'))
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created successfully"}), 201

@app.route('/tasks/<int:task_id>/complete',methods=['PUT'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed=True
        task.date_completed=db.func.current_date()
        db.session.commit()
        return jsonify({"message": "Task marked as completed"}),200
    else:
        return jsonify({"message": "Task not found"}),404

@app.route('/task_percentage/<string:date>', methods=['GET'])
def get_task_percentage(date):
    completed_tasks = Task.query.filter_by(date_completed=date, completed=True).count()
    total_tasks = Task.query.filter_by(date_completed=date).count()
    if total_tasks > 0:
        percentage = (completed_tasks / total_tasks) * 100
    else:
        percentage = 0
    return jsonify({"date": date, "percentage": percentage, "made_by": "Made by Hemant Garg"}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

#made by Hemant Garg


