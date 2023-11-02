from django.shortcuts import render 
from django.views.generic import *
from .models import Task,TaskPhoto
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
# def home(request):
#      return render(request,'tasks/home.html') 
# Implement the functionality

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'tasks/tasks_detail.html'
    context_object_name = 'task'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        task_photos = TaskPhoto.objects.filter(task=task)
        context['task_photos'] = task_photos
        return context

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/tasks_create.html'
    success_url = reverse_lazy('TaskListView')
    context_object_name = 'form'
    
    
    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        self.success_url = task.get_absolute_url()
        return super().form_valid(form)
  
  
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/tasks_create.html'
    success_url = reverse_lazy('TaskListView')
    

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        self.success_url = post.get_absolute_url()  
        return super().form_valid(form)
    
class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy('TaskListView')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
    
# TaskPhoto   
class TaskPhotoCreateView(LoginRequiredMixin,CreateView):
    model = TaskPhoto
    form_class = TaskPhotoForm
    template_name = 'tasks/tasks_photo_create.html'

    def get_success_url(self):
        task_id = self.kwargs['task_id']
        return reverse('TaskDetailView', kwargs={'pk': task_id})

    def form_valid(self, form):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        if task.user != self.request.user:
            return HttpResponseRedirect(reverse('TaskDetailView', kwargs={'pk': self.kwargs['task_id']}))


        form.instance.task = task
        return super().form_valid(form)
    
class TaskPhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskPhoto
    form_class = TaskPhotoForm
    template_name = 'tasks/tasks_photo_create.html'

    def get_success_url(self):
        task_id = self.kwargs['task_id']
        return reverse('TaskDetailView', kwargs={'pk': task_id})

    def get_object(self, queryset=None):
        task_photo = super().get_object(queryset)
        if task_photo.task.user != self.request.user:
            return HttpResponseRedirect(reverse('TaskDetailView', kwargs={'pk': self.kwargs['task_id']}))
        return task_photo

    def form_valid(self, form):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)
        if task.user != self.request.user:
            return HttpResponseRedirect(reverse('TaskDetailView', kwargs={'pk': self.kwargs['task_id']}))

        form.instance.task = task
        return super().form_valid(form)
    
class TaskPhotoDeleteView(DeleteView):
    model = TaskPhoto
    # success_url = reverse_lazy('TaskDetailView', kwargs={'pk': task_id})
    def get_success_url(self):
        task_id = self.kwargs['task_id']
        return reverse('TaskDetailView', kwargs={'pk': task_id})

    def get_object(self, queryset=None):
        task_photo = super().get_object(queryset)
        task = task_photo.task

        if task.user != self.request.user:
            return HttpResponseRedirect(reverse('TaskDetailView', kwargs={'pk': self.kwargs['task_id']}))

        return task_photo

    def delete(self, request, *args, **kwargs):
        task_photo = self.get_object()
        task_id = self.kwargs['task_id']
        task_photo.delete()
        return HttpResponseRedirect(reverse('TaskDetailView', kwargs={'pk': task_id}))

# Django rest framework
# Create the REST API views:
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.generics import *
from rest_framework import permissions



class TaskListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        posts = Task.objects.all().order_by('-created_at')
        serializer = TaskSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializerCreateUpdate(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  
    
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TaskSerializer(instance)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = TaskSerializerCreateUpdate(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        pk = kwargs.get('pk')
        queryset = Task.objects.get(id = pk )
        serializer = TaskSerializer(queryset,many=False)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        try:
            task = Task.objects.get(id=pk)
            if task:
                task.delete()
                return Response("Post deleted", status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("Post not found", status=status.HTTP_404_NOT_FOUND)
        
        
        
# Task photo
class TaskPhotoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  
    
    def get(self, request, task_id, pk=None):
        if pk is not None:
            task_photo = TaskPhoto.objects.filter(task_id=task_id, pk=pk).first()
            if not task_photo:
                return Response({'message': 'TaskPhoto not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = TaskPhotoSerializer(task_photo)
        else:
            task_photos = TaskPhoto.objects.filter(task_id=task_id)
            serializer = TaskPhotoSerializer(task_photos, many=True)
        return Response(serializer.data)

 
    def post(self, request, task_id):
        task = Task.objects.filter(pk=task_id).first()
        # print(task)
        # return Response({"test":task.id})
        
        if not task:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskPhotoSerializerCreateUpdate(data=request.data)
        if serializer.is_valid():
            serializer.save(task = task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, task_id, pk):
        task_photo = TaskPhoto.objects.filter(task_id=task_id, pk=pk).first()
        if not task_photo:
            return Response({'message': 'TaskPhoto not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskPhotoSerializerCreateUpdate(task_photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, pk):
        task_photo = TaskPhoto.objects.filter(task_id=task_id, pk=pk).first()
        if not task_photo:
            return Response({'message': 'TaskPhoto not found'}, status=status.HTTP_404_NOT_FOUND)
        task_photo.delete()
        return Response({'message': 'TaskPhoto deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
