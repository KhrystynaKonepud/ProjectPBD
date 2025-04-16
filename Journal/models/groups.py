# models/group.py
from mongoengine import Document, StringField, ListField, ReferenceField
from .student import Student

class Group(Document):
    name = StringField(required=True, unique=True)
    students = ListField(ReferenceField(Student))

    def __str__(self):
        return self.name
