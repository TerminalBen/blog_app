from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
    """Renders a list of posts, using the custom object manager

    Args:
        request ([type]): [description]
    """
    posts =  Post.published.all()
    render(request,'blog/post/list.html',{'posts':posts})

def post_detail(request,year,month,day,post):
    """[summary]

    Args:
        request ([type]): [description]
        year ([type]): [description]
        month ([type]): [description]
        day ([type]): [description]
        post ([type]): [description]
    """
    post = get_object_or_404(Post,slug=post,status ='Published',publish__year = year,publish__month = month, publish__day = day)
    render(request,'blog/post/detail.html',{'post',post})


