from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/serena/Desktop/Projects/toDo/todo.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


# server side
@app.route('/')
def index():
    incomplete = todos = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()

    return render_template('index.html', todos=todos, incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))
    # return '<h1>{}</h1>'.format(request.form['todoitem']) # now we know it was received


@app.route('/complete/<id>')
def complete(id):
    # return '<h1>{}</h1>'.format(id) # confirm it receives id
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'))

# Resume with checkboxes:
# @app.route('/update', methods=['POST'])
# def update():
#    print(request.form)
#    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)