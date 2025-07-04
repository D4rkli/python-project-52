from django import forms
from .models import Task, Label

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
