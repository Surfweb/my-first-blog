# -*- coding: utf-8 -*-

from django import forms
from .models import Post



class PostForm(forms.ModelForm): # PostForm - name to we form

    class Meta:
        model = Post 	# set model, defening to create form 
        fields = ('title', 'text',) 	# set row, defening field form
        
        

