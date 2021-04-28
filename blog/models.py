"""models creation:
    1º- Post model
    2º- Category (not done)
"""

from django.db import models
from django.db.models.expressions import OrderBy
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    """[summary]

    Args:
        models ([type]): [description]

    Vars:


    Returns:
        [type]: [description]
    """
    STATUS_CHOICES =('draft','Draft'),('published','Published')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body =models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    likes = models.IntegerField(default=0,editable=True)
    class Meta:
        ordering=('-publish','-likes')

    def __str__(self) -> str:
        """[summary]

        Returns:
            str: [description]
        """
        return self.title

