# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
      name=models.CharField(max_length=50, unique=True)
      description=models.CharField(max_length=255) 
      def __str__(self):
          return self.name

class Topic(models.Model):
      subject=models.CharField(max_length=255)
      last_updated=models.DateTimeField(auto_now_add=True)
      boards=models.ForeignKey(Board,on_delete=models.CASCADE,related_name='topic')
      starter=models.ForeignKey(User,on_delete=models.CASCADE,related_name='topic')
      def __str__(self):
          return self.subject

class Post(models.Model):
      message=models.TextField(max_length=255)
      topic=models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='post')
      created_at=models.DateTimeField(auto_now_add=True)
      updated_at=models.DateTimeField(null=True)
      created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='post')
      updated_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='+')
      def __str__(self):
          return self.message




      
      
