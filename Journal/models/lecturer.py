from mongoengine import Document, StringField, EmailField, ListField, ReferenceField

class Lecturer(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True, default="lecturer")

    subjects = ListField(ReferenceField('Subjects'))
    groups = ListField(ReferenceField('Groups'))
    created_journals = ListField(ReferenceField('Journal'))

    def __str__(self):
        return self.name
