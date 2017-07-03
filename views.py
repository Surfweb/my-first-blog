# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect

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