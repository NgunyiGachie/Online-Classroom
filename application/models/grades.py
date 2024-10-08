from database import db
from sqlalchemy.orm import validates
from datetime import datetime

class Grade(db.Model):
    __tablename__  = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)

    student = db.relationship('Student', back_populates='grade')
    course = db.relationship('Course', back_populates='grade')
    submission = db.relationship('Submission', back_populates='grade', cascade='all, delete-orphan')

    @validates('grade')
    def validate_grade(self, key, grade):
        if grade is None:
            raise AssertionError('Grades cannot be None')
        if not isinstance(grade, int):
            raise AssertionError("Grades must be an integer")
        if grade < 1 or grade > 100:
            raise ValueError("Grades must be between 1 and 100")
        return grade
    
    @validates('date_posted')
    def validate_dates(self, key, value):
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'grade': self.grade,
            'date_posted': self.date_posted
        }
    
    def __repr__(self):
        """Return string representation of the model instance."""
        return f"<Grade {self.id}>"