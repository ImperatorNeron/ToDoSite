from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateTaskForm, SignUpForm, ProfileEditForm
from .models import *
from django.http import Http404


class Index(TemplateView):
    """ Main page """
    template_name = 'task/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_photos'] = SiteImages.objects.all()
        return context


# todo: use better naming, such as TaskView AND
# class based views are recommended when you need to handle multiple requests at one point
# check https://stackoverflow.com/questions/27688107/how-does-class-based-view-with-multiple-methods-work-with-urls-in-django
class TaskView(LoginRequiredMixin, ListView):
    """ Show all tasks """
    template_name = 'task/MyTasks.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('is_complete', '-pk')

    # Filter by user, perform a get request for the field with a search for records.
    # Count the number of completed tasks that are on the list
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__contains=search_input)
        context['search_input'] = search_input
        context['done'] = Task.objects.filter(user=self.request.user, is_complete=True).count()
        context['all'] = Task.objects.filter(user=self.request.user).count()
        return context

    # Mark as done or not done
    @staticmethod
    def complete(request, pk):
        # Check user
        if request.user != Task.objects.get(pk=pk).user:
            raise Http404
        data = get_object_or_404(Task, pk=pk)
        # Add and subtract + save so that a point is not lost when deleting a task
        if not data.is_complete:
            data.is_complete = True
            request.user.score += 1
        else:
            data.is_complete = False
            request.user.score -= 1
        request.user.save()
        data.save()
        return redirect('task_page')


class CreateTask(LoginRequiredMixin, CreateView):
    """ Create task """

    template_name = 'task/CreateTask.html'
    form_class = CreateTaskForm
    success_url = reverse_lazy('task_page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class DeleteTask(LoginRequiredMixin, DeleteView):
    """Delete task or all tasks"""

    model = Task
    template_name = 'task/DeleteTask.html'
    success_url = reverse_lazy('task_page')

    # We check whether the user has access to this page
    # (so that it is not possible to go to someone else's tasks through the link)
    # If it is not him, we raise an error

    # todo: that's cool that you raised error here
    # but check if it could be solved just using get_queryset()
    def get_object(self, queryset=None):
        obj = super(DeleteTask, self).get_object()
        if obj.user != self.request.user:
            raise Http404('Точно працює')
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = 'Ви впевнені, що хочете видалити цей запис?'
        return context


class UpdateTask(LoginRequiredMixin, UpdateView):
    """ Update task """

    template_name = 'task/CreateTask.html'
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy('task_page')

    def get_object(self, queryset=None):
        obj = super(UpdateTask, self).get_object()
        if obj.user != self.request.user:
            raise Http404('Точно працює')
        return obj


class LoginAccount(LoginView):
    """Login"""
    template_name = 'task/Login.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('main_page')


class RegisterAccount(FormView):
    """Registration"""
    template_name = 'task/Registration.html'
    form_class = SignUpForm
    success_url = reverse_lazy('main_page')

    # If you have registered, log out of the old account and switch to the new one
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            logout(self.request)
            login(self.request, user)
        return super(RegisterAccount, self).form_valid(form)


# Власний профіль
class ProfileCheck(LoginRequiredMixin, DetailView):
    """ Your profile """
    model = CustomUser
    template_name = 'task/ProfileCheck.html'
    context_object_name = 'profile'

    # Checking the user/raising an error
    def get_object(self, queryset=None):
        obj = super(ProfileCheck, self).get_object(queryset=queryset)
        if obj.username != self.request.user.username:
            raise Http404('Точно працює')
        return obj


class ProfileEdit(LoginRequiredMixin, UpdateView):
    """ Editing profile """
    template_name = 'task/ProfileEdit.html'
    model = CustomUser
    form_class = ProfileEditForm
    success_url = reverse_lazy('main_page')

    # Checking the user/raising an error
    def get_object(self, queryset=None):
        obj = super(ProfileEdit, self).get_object(queryset=queryset)
        if obj.username != self.request.user.username:
            raise Http404('Точно працює')
        return obj


class Rating(ListView):
    """ Rating page """
    template_name = 'task/Rating.html'
    context_object_name = 'user_rating'
    model = CustomUser

    # the first 20 people by points
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_rating'] = context['user_rating'].order_by('-score', '-username')[:20]
        if self.request.user.is_authenticated:
            context['user_position'] = list(context['user_rating']).index(self.request.user) + 1
        return context


class CheckSomebodyProfile(DetailView):
    """ Check somebody`s profile from rating """
    template_name = 'task/CheckSomebodyProfile.html'
    model = CustomUser
    context_object_name = 'profile'


# if 404 Error, redirect to page with tasks
def page_not_found_view(request, exception):
    return redirect('task_page')


# Delete all records that have been executed from the list
def delete_all_completed_tasks(request):
    if request.method == 'POST':
        # We take all records of this user that have been completed and delete them
        Task.objects.filter(user=request.user, is_complete=True).delete()
        return redirect('task_page')
    return render(request, 'task/DeleteDoneTasks.html',
                  context={'text': 'Ви впевнені, що хочете видалити всі виконані записи?'})
