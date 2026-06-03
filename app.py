from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



app = Flask(__name__)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/student_crud')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Display all students"""
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """Add a new student"""
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        class_name = request.form['class_name']
        address = request.form['address']

        # Check if roll number already exists
        existing_student = Student.query.filter_by(roll_no=roll_no).first()
        if existing_student:
            flash('Roll number already exists!', 'error')
            return redirect(url_for('add_student'))

        new_student = Student(name=name, roll_no=roll_no, class_name=class_name, address=address)
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    """Edit an existing student"""
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        class_name = request.form['class_name']
        address = request.form['address']

        # Check if roll number already exists (excluding current student)
        existing_student = Student.query.filter_by(roll_no=roll_no).filter(Student.id != id).first()
        if existing_student:
            flash('Roll number already exists!', 'error')
            return redirect(url_for('edit_student', id=id))

        student.name = name
        student.roll_no = roll_no
        student.class_name = class_name
        student.address = address

        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    """Delete a student"""
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)