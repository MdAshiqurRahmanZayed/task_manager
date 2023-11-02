from django import forms 
from .models import Task,TaskPhoto


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description','due_date', 'priority', 'is_complete'] 
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

        
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['priority'].widget.attrs['class'] = 'form-control'
        self.fields['is_complete'].widget.attrs['class'] = 'form-check-input'

class TaskPhotoForm(forms.ModelForm):
    class Meta:
        model = TaskPhoto
        fields = ['photo'] 
    def __init__(self, *args, **kwargs):
        super(TaskPhotoForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['class'] = 'form-control'

