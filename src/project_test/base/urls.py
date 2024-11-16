from django.urls import path
from .views import PendingsList, CreateTask, EditTask, DeleteTask, Logueo, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [path('', PendingsList.as_view(), name='tasks'),
               path('login/', Logueo.as_view(), name='login'),
               path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
               path('register_user/', RegisterPage.as_view(), name='register_user'),
               path('create-task/', CreateTask.as_view(), name='create-task'),
               path('edit-task/<int:pk>', EditTask.as_view(), name='edit-task'),
               path('delete-task/<int:pk>', DeleteTask.as_view(), name='delete-task')]