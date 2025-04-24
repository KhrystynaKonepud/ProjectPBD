from mongoengine import Document, StringField, ListField, ReferenceField

class Groups(Document):
    name = StringField(required=True, unique=True)
    students = ListField(ReferenceField('Students'))

    def __str__(self):
        return self.name
