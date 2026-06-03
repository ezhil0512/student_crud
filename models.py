from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    class_name = db.Column(db.String(50), nullable=False)  # 'class' is a reserved keyword in Python
    address = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'