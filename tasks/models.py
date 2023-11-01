from django.db import models
from Accounts.models import Account

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    class Meta:
        abstract = True

PRIORITY_CHOICES = [
     ('Low', 'Low'),
     ('Medium', 'Medium'),
     ('High', 'High'),
]
class Task(TimeStampedModel):
    user = models.ForeignKey(Account, on_delete=models.CASCADE) 
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
         return self.title
    
    
class TaskPhoto(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/task_photos/')
    
    def __str__(self):
         return self.task.title
