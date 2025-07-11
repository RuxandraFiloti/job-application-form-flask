from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapp123" # Set a secret key for session management, is good for untracking by the hackers
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db" #for mysql, replace 'sqlite' with 'mysql'
app.config["MAIL_SERVER"] = "smtp.gmail.com" # Set your mail server here if you are using Flask-Mail
app.config["MAIL_PORT"] = 465 # Set your mail port here if you are using Flask-Mail
app.config["MAIL_USE_SSL"] = True # Set to True if you are using Flask-Mail
app.config["MAIL_USERNAME"] = "adaflori0207@gmail.com"
app.config["MAIL_PASSWORD"] = "lprp edby ihef bpuq" # Set your mail password here if you are using Flask-Mail


db = SQLAlchemy(app) # Initialize the database

mail = Mail(app) # Initialize Flask-Mail


class Form(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80)) 




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]


        form = Form(first_name=first_name, 
                    last_name=last_name, 
                    email=email, 
                    date=date_obj, 
                    occupation=occupation)
        db.session.add(form) # Add the form data to the session
        db.session.commit() # Commit the session to save the data to the database

        message_body = f"Thank you for your submission, {first_name}! " \
                        f"Here are your details:\n{first_name}\n{last_name}\n{date}\n" \
                        f"Thank you!"

        # Send an email notification (optional)
        message = Message(subject="Job Application Received",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        flash(f"{first_name}, your form submitted successfully!", "success") # Flash a success message

       

        # Here you would typically process the form data, e.g., save it to a database or send an email
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context(): #db migration
        db.create_all()
        app.run(debug=True, port=4200)