from django.urls import path
from .views import *
urlpatterns = [
    # path("",home,name='home'),
    path("",TaskListView.as_view(),name='TaskListView'),
    path("<int:pk>/",TaskDetailView.as_view(),name='TaskDetailView'),
    path("task-create/",TaskCreateView.as_view(),name='TaskCreateView'),
    path("task-update/<int:pk>/",TaskUpdateView.as_view(),name='TaskUpdateView'),
    path("task-delete/<int:pk>/",TaskDeleteView.as_view(),name='TaskDeleteView'),
    
    #TaskPhoto
    path('tasks/<int:task_id>/add-photo/', TaskPhotoCreateView.as_view(), name='TaskPhotoCreateView'),   
    path('tasks/<int:task_id>/photo/<int:pk>/update/', TaskPhotoUpdateView.as_view(), name='TaskPhotoUpdateView'), 
    path('tasks/<int:task_id>/photo/<int:pk>/delete/', TaskPhotoDeleteView.as_view(), name='TaskPhotoDeleteView'),
    #API
    path("api/",TaskListCreateAPIView.as_view(),name='TaskListCreateAPIView'),
    path("api/task/<int:pk>/",TaskRetrieveUpdateDestroyAPIView.as_view(),name='TaskRetrieveUpdateDestroyAPIView'),
    
    # task photo
    path('api/task/<int:task_id>/photo/', TaskPhotoAPIView.as_view(), name='TaskPhotoAPIView'),
    path('api/task/<int:task_id>/photo/<int:pk>/', TaskPhotoAPIView.as_view(), name='TaskPhotoAPIView'),

    
]
