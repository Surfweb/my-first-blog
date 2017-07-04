# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'), # detail info for post
	url(r'^post/new/$', views.post_new, name='post_new'),	# Add new post
	url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),  # url для редактирования формы
	url(r'^register/$', views.RegisterFormView.as_view(), name='register_user'), # Регистрация
	url(r'^login/$', views.LoginFormView.as_view(), name='login'), # Вход
	url(r'^logout/$', views.LogoutView.as_view(), name='logout'), # Выход
]