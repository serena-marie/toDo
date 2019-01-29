import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

proj_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:////{}".format(os.path.join(proj_dir, "todo.db"))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    # incomplete = todos = Todo.query.filter_by(complete=False).all()
    # complete = Todo.query.filter_by(complete=True).all()
    # todos = Todo.query.all()
    # return render_template('index.html', todos=todos, incomplete=incomplete, complete=complete)
    todos = Todo.query.filter_by(complete=False).all()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))
    # return '<h1>{}</h1>'.format(request.form['todoitem']) # now we know it was received


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        selected = request.form.get("itemTest")
        print(selected)
        todo = Todo.query.filter_by(id=int(selected)).first()  # because expecting only 1 itemsho
        todo.complete = True
        db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)