# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect

#Регистрация пользователя
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

# спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm
# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login

# Выход
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout


# Create your views here.

def post_list(request):
    # Получаем список всех записей в Post отсортированных в обратном порядке по дате публикации
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
	
# предсталение для конкртного поста
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
	
# предсталение для формы
def post_new(request):
        if request.method == "POST":		# Возвращаемся к форме, после добавления поста
            form = PostForm(request.POST) 	# Получаем данные из формы request.POST
            if form.is_valid():				# Валидация полей формы
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()					# Сохраняем форму
                return redirect('post_detail', pk=post.pk)
        else:		# Возвращает пустую форму
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

# представление для редактирования поста
def post_edit(request, pk):
        post = get_object_or_404(Post, pk=pk)	# получаем из модели Post, запись по pk
        if request.method == "POST":
            form = PostForm(request.POST, instance=post) 
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
        
        
#Регистрация пользователя
class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "blog/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)
        
# Авторизация
class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "blog/login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)
        
# Выход пользователя
class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")
