"""models creation:
    1º- Post model
    2º- Category (not done)
"""

from django.db import models
#from django.db.models.expressions import OrderBy
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """custom model manager Class with a method to retrieve published posts

    Args:
        models ([model]): [django model]
    """
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status = 'published')


class Post(models.Model):
    """[summary]

    Args:
        models ([type]): [description]

    Vars:


    Returns:
        [type]: [description]
    """
    tags = TaggableManager()
    STATUS_CHOICES =('draft','Draft'),('published','Published')
    CATEGORY_CHOICES = ('tech','Tech'),('actualidade','Actualidade')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    #body =models.TextField()
    body = RichTextField(blank=True,null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    category =models.CharField(max_length=20,choices=CATEGORY_CHOICES,default='')
    likes = models.IntegerField(default=0,editable=True)
    class Meta:
        ordering=('-publish','-likes')

    def __str__(self) -> str:
        """[summary]

        Returns:
            str: [description]
        """
        return self.title

    objects = models.Manager() #default manager
    published = PublishedManager() #custom manager

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[ self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug])
    

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'