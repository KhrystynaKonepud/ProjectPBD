from mongoengine import (
    Document, StringField, EmailField, ListField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField, IntField
)
from .journal import Journal  # для зв'язку з журналами
from .groups import Groups


# Оцінка студента за конкретним журналом
class GradeEntry(EmbeddedDocument):
    journal_id = ReferenceField(Journal, required=True)  # Посилання на журнал
    total = IntField(default=0)  # Загальна оцінка студента за журналом

# Основний клас студента
class Students(Document):
    name = StringField(required=True)  # Ім'я студента
    email = EmailField(required=True, unique=True)  # Електронна пошта (унікальна)
    password = StringField(required=True)  # Пароль студента

    group = ReferenceField(Groups, required=True)  # Посилання на групу, до якої належить студент
    grades = ListField(EmbeddedDocumentField(GradeEntry), default=[])  # Оцінки за журнали (список GradeEntry)
    average = IntField(default=0)  # Середній бал (можна обчислювати вручну або автоматично)

    def __str__(self):
        return self.name
