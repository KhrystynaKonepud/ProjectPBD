from mongoengine import Document, StringField, IntField, ListField, ReferenceField

class Subjects(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    lecturer = ListField(ReferenceField('Lecturer'))
    groups = ListField(ReferenceField('Groups'))
    hours = IntField()
    exam_type = StringField(choices=["Екзаменаційна", "Залікова", "Диференційований залік"])
    class_types = ListField(StringField(choices=["Лекції", "Лабораторні", "Практичні"]))

    def __str__(self):
        return self.name
