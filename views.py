# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils import timezone
from .models import Post

# Create your views here.

def post_list(request):
    # Получаем список всех записей в Post отсортированных по дате публикации
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
