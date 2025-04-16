from mongoengine import Document, StringField, EmailField, ListField, ReferenceField
from .models import Subjects, Groups, Journal

class Lecturer(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    subjects = ListField(ReferenceField('Subjects'))  # або 'Subject', якщо ще не імпортований
    groups = ListField(ReferenceField('Groups'))
    created_journals = ListField(ReferenceField('Journal'))

    def __str__(self):
        return self.name
