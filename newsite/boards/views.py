# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm
from .reply_form import PostForm
@login_required
def home(request):
   boards=Board.objects.all()
   return render(request,'home.html',{'boards':boards})

@login_required
def board_topics(request,pk):
    board=get_object_or_404(Board,pk=pk)
    topic = board.topic.order_by('-last_updated').annotate(replies=Count('post'))
    return render(request, 'topics.html', {'board': board,'topic': topic})
@login_required
def new_topics(request,pk):
    board=get_object_or_404(Board,pk=pk)
    if request.method=='POST':
       form=NewTopicForm(request.POST)
       if form.is_valid():
          topic=form.save(commit=False)
          topic.boards=board
          topic.starter=request.user
          topic.save()
          post=Post.objects.create(
               message=form.cleaned_data.get('message'),
               topic=topic,
               created_by=request.user)
          return redirect('topic_post',pk=pk,topic_pk=topic_pk)
    else:
       form=NewTopicForm()   
    
    return render(request, 'posts.html', {'board': board,'form':form})
@login_required
def topic_post(request,pk,topic_pk):
    topic=get_object_or_404(Topic,boards__pk=pk,pk=topic_pk)
    topic.watch +=1
    topic.save()
    return render(request,'topic_post.html',{'topic':topic})

@login_required
def reply_post(request,pk,topic_pk):
    topic=get_object_or_404(Topic,boards__pk=pk,pk=topic_pk)
    form=PostForm()
    if request.method=='POST':
       form=PostForm(request.POST)
       if form.is_valid():
          post=form.save(commit=False)
          post.topic=topic
          post.created_by=request.user
          post.save()
          return redirect('topic_post',pk=pk,topic_pk=topic_pk)
       else:
          form=PostForm(request.POST)
    return render(request,'reply_post.html',{'topic':topic,'form':form})

          
    






