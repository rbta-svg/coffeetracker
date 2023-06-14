from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func



# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database and the SQLAlchemy ORM
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model for the User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    @property
    def coffee_count(self):
        return Coffee.query.filter_by(user_id=self.id).count()

# Model for the Coffee
class Coffee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        action = request.form['action']

        user = User.query.filter_by(name=name).first()

        # If the user doesn't exist, create them
        if not user:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()  # Commit now so that user.id is assigned

        if action == 'Add Coffee':
            coffee = Coffee(user_id=user.id)  # Here's the change
            db.session.add(coffee)
        elif action == 'Remove Coffee':
            coffee = Coffee.query.filter_by(user_id=user.id).first()
            if coffee:
                db.session.delete(coffee)

        db.session.commit()

        return redirect(url_for('index', name=name))

    name = request.args.get('name')
    user = User.query.filter_by(name=name).first() if name else None

    # Fetch all users and their coffee count
    users = User.query.all()

    return render_template('index.html', user=user)

@app.route('/monthly-list', methods=['GET'])
def monthly_list():
    # To be implemented: Show the list of coffees for the current month.
    pass

if __name__ == '__main__':
    app.run(debug=True)

