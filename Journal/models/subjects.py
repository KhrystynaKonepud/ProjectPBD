from mongoengine import Document, StringField, IntField, ListField, ReferenceField
from .lecturer import Lecturer
from .group import Group


class Subjects(Document):

    name = StringField(required=True, unique=True)
    description = StringField()
    lecturer = ReferenceField(Lecturer, required=True)
    groups = ListField(ReferenceField(Group))
    hours = IntField()
    exam_type = StringField(choices=["Екзаменаційна", "Залікова", "Диференційований залік"])
    class_types = ListField(StringField(choices=["Лекції", "Лабораторні", "Практичні"]))

    def __str__(self):
        return self.name

