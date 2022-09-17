from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', Index.as_view(), name="main_page"),
    path('tasks/', TaskView.as_view(), name="task_page"),
    path('task-creation/', CreateTask.as_view(), name="task_create"),
    path('deleting-task/task-<int:pk>', DeleteTask.as_view(), name="task_delete"),
    path('task-update/task-<int:pk>', UpdateTask.as_view(), name="edit_task"),
    path('login/', LoginAccount.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page="main_page"), name="logout"),
    path('registration/', RegisterAccount.as_view(), name="registration"),
    path('<slug:slug>/profile/', ProfileCheck.as_view(), name="check"),
    path('<slug:slug>/profile-editing/', ProfileEdit.as_view(), name="edit"),
    path('rating/', Rating.as_view(), name="rating"),
    path('completion/task-<int:pk>', TaskView.complete, name='complete'),
    path('view-profile/<slug:slug>/', CheckSomebodyProfile.as_view(), name='check_somebody'),
    path('deleting-completed-tasks/', delete_all_completed_tasks, name='DeleteDoneTasks'),
]
