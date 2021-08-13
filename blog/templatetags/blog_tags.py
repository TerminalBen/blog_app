from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag()
def total_posts():
    return Post.published.count()

@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-publish')[:count]
    
    return {
        "latest_posts": latest_posts
    }

@register.inclusion_tag("blog/post/most_commented_posts.html")
def get_most_commented_posts(count=5):
    most_commented_posts = Post.published.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]
    return{"most_commented_posts":most_commented_posts}

# @register.simple_tag()
# def get_most_commented_posts(count=5):
#     most_commented_posts = Post.published.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]
#     return most_commented_posts 

@register.inclusion_tag("blog/post/most_liked_posts.html")
def get_most_liked_posts(count=5):
    most_liked_posts = Post.published.annotate(total_likes = Count('likes')).order_by('-total_likes')[:count]
    return {"most_liked_posts":most_liked_posts}