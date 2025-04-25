from django import forms
from datetime import date

class JournalForm(forms.Form):
    subject = forms.CharField(label="Предмет", max_length=100)
    group = forms.CharField(label="Група", max_length=100)
    total_points = forms.IntegerField(label="Кількість балів", min_value=0)

    session_types = forms.CharField(
        label="Типи занять (через кому)",
        required=False,
        help_text="Наприклад: лекція, практика, лаба"
    )
    max_points_per_session = forms.CharField(
        label="Макс. бали за заняття (через кому)",
        required=False,
        help_text="Наприклад: 10,10,20"
    )
    deadlines = forms.CharField(
        label="Дедлайни (у форматі РРРР-ММ-ДД через кому)",
        required=False,
        help_text="Наприклад: 2025-05-01,2025-06-01"
    )
    late_penalties = forms.CharField(
        label="Штрафи за запізнення (через кому)",
        required=False,
        help_text="Наприклад: 0.1,0.2"
    )
    comments_enabled = forms.BooleanField(label="Дозволити коментарі", required=False)

    def clean_session_types(self):
        data = self.cleaned_data['session_types']
        return [s.strip() for s in data.split(',')] if data else []

    def clean_max_points_per_session(self):
        data = self.cleaned_data['max_points_per_session']
        return [int(p.strip()) for p in data.split(',')] if data else []

    def clean_deadlines(self):
        data = self.cleaned_data['deadlines']
        try:
            return [date.fromisoformat(d.strip()) for d in data.split(',')] if data else []
        except ValueError:
            raise forms.ValidationError("Формат дати має бути РРРР-ММ-ДД")

    def clean_late_penalties(self):
        data = self.cleaned_data['late_penalties']
        return [float(p.strip()) for p in data.split(',')] if data else []
