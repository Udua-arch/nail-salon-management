from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from utils.helpers import get_popular_services, get_peak_hours
from datetime import datetime

app = Flask(__name__)
app.secret_key = "nail_salon_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nail_salon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

appointments_list = []  



class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    preferences = db.Column(db.Text)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    staff = db.Column(db.String(50))

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer)  


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        preferences = request.form.get('preferences', "")
        new_customer = Customer(name=name, phone=phone, email=email, preferences=preferences)
        try:
            db.session.add(new_customer)
            db.session.commit()
            flash("Customer added successfully!", "success")
        except Exception as e:
            flash("Error adding customer: " + str(e), "danger")
    all_customers = Customer.query.all()
    return render_template('customers.html', customers=all_customers)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        customer = request.form['customer']
        service = request.form['service']
        date = request.form['date']
        time = request.form['time']
        staff = request.form['staff']

        
        new_appointment = {
            "customer": customer,
            "service": service,
            "date": date,
            "time": time,
            "staff": staff
        }
        appointments_list.append(new_appointment)  

    return render_template('appointments.html', appointments=appointments_list)


@app.route('/services', methods=['GET', 'POST'])
def services():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        duration = request.form['duration']
        new_service = Service(name=name, price=price, duration=duration)
        try:
            db.session.add(new_service)
            db.session.commit()
            flash("Service added successfully!", "success")
        except Exception as e:
            flash("Error adding service: " + str(e), "danger")
    all_services = Service.query.all()
    return render_template('services.html', services=all_services)


if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()  
    
    app.run(debug=True)
