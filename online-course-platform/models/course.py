# models/course.py
class Course:
    def __init__(self, id, title, instructor, price):
        self.id = id
        self.title = title
        self.instructor = instructor
        self.price = price
