from rest_framework import serializers
from .models import Task,TaskPhoto
from Accounts.serializers import AccountSerializer


class TaskSerializer(serializers.ModelSerializer):
     user = AccountSerializer(many=False)
     class Meta:
          model = Task
          fields = ['id','user','title','description','due_date','priority','is_complete']
          read_only_fields = ['user']

      
class TaskSerializerCreateUpdate(serializers.ModelSerializer):
     class Meta:
          model = Task
          fields = ['title','description','due_date','priority','is_complete']
          


          
class TaskPhotoSerializer(serializers.ModelSerializer):
     task = TaskSerializer()
     class Meta:
          model = TaskPhoto
          fields = '__all__'
class TaskPhotoSerializerCreateUpdate(serializers.ModelSerializer):
     class Meta:
          model = TaskPhoto
          fields = ['photo']
          