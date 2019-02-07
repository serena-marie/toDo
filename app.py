#  To Be Completed
# [ ] Update Multiple
# [x] Display Completed under completed
# [x] Remove
# [ ] Track Date ?
# [ ] Track Time Completed
# [x] one-to-many relationship
#   [ ] update routes to correctly do the dang thing
# [x] Allow for multiple users
# C(reate)-R(ead)-U(pdate)-D(elete)

import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# database path
proj_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:////{}".format(os.path.join(proj_dir, "todo.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
db = SQLAlchemy(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    todos = db.relationship('Todo', backref='user', lazy=True)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# routes
@app.route('/')
def index():
    # Adding Guest user if not already in table
    if User.query.filter_by(name="Guest").first() is None:
        # args = { id=1, name="Guest"}
        guest_info = {'id': 1, 'name': 'Guest'}
        # adduser = User.create(**guest_info)
        adduser = User(**guest_info)
        db.session.add(adduser)
        db.session.commit()

    # Display
    incomplete = Todo.query.filter_by(complete=False).order_by(Todo.user_id).all()
    complete = Todo.query.filter_by(complete=True).order_by(Todo.user_id).all()
    # usr = User.query.order_by(User.id).first()
    # usr = Todo.query.with_parent(Todo.user_id);
    # user_display = User.query.filter_by(id=Todo.user_id).all()
    # user_display = User.query.order_by(Todo.user_id).all()
    # zip_data = zip(incomplete, user_display)
    # return render_template('index.html', incomplete=incomplete, complete=complete, user_display=user_display, zip_data=zip_data)
    return render_template('index.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    # return '<h1>{}</h1>'.format(request.form['username'])
    # The way this is set up - need to explicitly update user_id
    # todo = Todo(text=request.form['todoitem'], complete=False, user_id=request.form['user.name'])
    todo = Todo(text=request.form['todoitem'], complete=False, user_id=request.form['username'])

    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))
#     # return '<h1>{}</h1>'.format(request.form['todoitem']) # now we know it was received


@app.route('/new', methods=['POST'])
def new_member():
    # return '<h1>{}</h1>'.format(request.form['newname'])
    newUser = User(name=request.form['newname'])
    db.session.add(newUser)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        selected = request.form.get("itemTest")
        todo = Todo.query.filter_by(id=int(selected)).first()  # because expecting only 1 itemsho
        todo.complete = True
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/remove', methods=['POST'])
def remove():
    selected = request.form.get("itemTest")
    todo = Todo.query.filter_by(id=int(selected)).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
