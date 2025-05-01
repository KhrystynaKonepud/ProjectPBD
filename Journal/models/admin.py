from mongoengine import Document, StringField, EmailField, ListField

class Admin(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default='admin')
    
    permissions = ListField(StringField())

    def __str__(self):
        return self.name

