# Flask Routes (continued)
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medicine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Medicine Model
class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    medicines = Medicine.query.all()
    today = datetime.now()
    return render_template('index.html', medicines=medicines, today=today)

@app.route('/add_medicine_page')
def add_medicine_page():
    return render_template('add_medicine.html')

@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    if request.method == 'POST':
        name = request.form['name']
        expiry_date_str = request.form['expiry_date']
        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
        
        new_medicine = Medicine(name=name, expiry_date=expiry_date)
        db.session.add(new_medicine)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/edit_medicine/<int:id>', methods=['GET', 'POST'])
def edit_medicine(id):
    medicine = Medicine.query.get(id)

    if request.method == 'POST':
        medicine.name = request.form['name']
        expiry_date_str = request.form['expiry_date']
        medicine.expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_medicine.html', medicine=medicine)

@app.route('/delete_medicine/<int:id>')
def delete_medicine(id):
    medicine = Medicine.query.get(id)
    db.session.delete(medicine)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
