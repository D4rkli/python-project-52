from .models import Status
from django import forms

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('name',)
        labels = {'name': 'Имя'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
