from mongoengine import (
    Document, StringField, EmailField, ListField, ReferenceField, IntField,
    EmbeddedDocument, EmbeddedDocumentField, BooleanField, DateField, FloatField
)

# --- Модель студента ---
class Students(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    group = ReferenceField('Groups')
    grades = ListField(IntField(), default=[])
    average = IntField(default=0)

    def __str__(self):
        return self.name


# --- Модель групи ---
class Groups(Document):
    name = StringField(required=True, unique=True)
    students = ListField(ReferenceField(Students))

    def __str__(self):
        return self.name


# --- Модель журналу для студентів ---
class JournalStudent(EmbeddedDocument):
    student_id = ReferenceField(Students, required=True)
    name = StringField()
    grades = ListField(IntField(), default=[])
    comments = ListField(StringField(), default=[])
    total = IntField(default=0)


class Journal(Document):
    lecturer_id = ReferenceField('Lecturer', required=True)
    subject = ReferenceField('Subjects', required=True)
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


# --- Модель викладача ---
class Lecturer(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    role = StringField(required=True, default="lecturer")

    subjects = ListField(ReferenceField('Subjects'))
    groups = ListField(ReferenceField(Groups))
    created_journals = ListField(ReferenceField(Journal))

    def __str__(self):
        return self.name


# --- Модель предметів ---
class Subjects(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    lecturer = ReferenceField(Lecturer, required=True)
    groups = ListField(ReferenceField(Groups))
    hours = IntField()
    exam_type = StringField(choices=["Екзаменаційна", "Залікова", "Диференційований залік"])
    class_types = ListField(StringField(choices=["Лекції", "Лабораторні", "Практичні"]))

    def __str__(self):
        return self.name
