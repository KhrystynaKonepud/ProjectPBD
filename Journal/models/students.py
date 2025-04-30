from mongoengine import Document, StringField, EmailField, ListField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField, IntField

class GradeEntry(EmbeddedDocument):
    journal_id = ReferenceField('Journal', required=True)
    total = IntField(default=0)

class Students(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    group = ReferenceField('Groups', required=False, null=True)
    grades = ListField(EmbeddedDocumentField(GradeEntry), default=[])
    average = IntField(default=0)

    def __str__(self):
        return self.name
