from mongoengine import (
    Document, EmbeddedDocument, StringField, IntField, ListField, BooleanField,
    ReferenceField, EmbeddedDocumentField, DateField, FloatField
)
#from .student import Student
from .lecturer import Lecturer
from .subjects import Subjects
from .groups import Groups

# Студент у журналі
class JournalStudent(EmbeddedDocument):
    student_id = ReferenceField(Student, required=True)
    name = StringField()
    grades = ListField(IntField(), default=[])
    comments = ListField(StringField(), default=[])
    total = IntField(default=0)

# Основний клас журналу
class Journal(Document):
    lecturer_id = ReferenceField(Lecturer, required=True)
    subject = ReferenceField(Subjects, required=True)
    group = ReferenceField(Groups, required=True)
    total_points = IntField(required=True)

    session_types = ListField(StringField())
    max_points_per_session = ListField(IntField())
    deadlines = ListField(DateField())
    late_penalties = ListField(FloatField(), default=[])

    comments_enabled = BooleanField(default=False)
    students = ListField(EmbeddedDocumentField(JournalStudent))

    def __str__(self):
        return f"Журнал: {self.subject.name} ({self.group.name})"
