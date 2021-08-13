from django.shortcuts import render, get_object_or_404
from .models import Post
#from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import emailPostForm,CommentForm,SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import  SearchVector

# Create your views here.

# def post_list(request):
#   object_list = Post.published.all()
#   paginator = Paginator(object_list, 3) # 3 posts in each page
#   page = request.GET.get('page')
#   try:
#       posts = paginator.page(page)
#   except PageNotAnInteger:
# # If page is not an integer deliver the first page
#       posts = paginator.page(1)
#   except EmptyPage:
# # If page is out of range deliver last page of results
#   posts = paginator.page(paginator.num_pages)
#   return render(request,'blog/post/list.html',{'page': page,'posts': posts})

class PostListView(ListView):
    """Renders a list of posts, using the custom object manager
        Paginator is now implemented
        Changed it to class based view instead of function based view
    Args:
        request ([type]): [description]
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name  = 'blog/post/list.html'


class TagListView(ListView):
    model = Post
    template_name  = 'blog/post/list.html'
    paginate_by = 3
    context_object_name = 'posts'

    def get_queryset(self):
        self.tags = get_object_or_404(Tag,slug=self.kwargs['tag_slug'])
        return Post.objects.filter(tags=self.tags)

    def get_context_data(self, **kwargs):
        context=super(TagListView, self).get_context_data(**kwargs)
        context['tag']=self.tags
        return context

class CategListView(ListView):
    #TODO
    pass

def post_share(request,post_id):
    """handles the Email form posts from .forms to send the email form

    Args:
        request (request): [description]
        post_id (post_id): [description]
    """
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    if request == 'POST':
        form = emailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recomends you read {post.title}"
            message = f"Read {post.title} at {post_url}.\n\n Comments:{cd['comments']}"
            send_mail(subject,message,'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form =emailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})


def post_detail(request,year,month,day,post):
    """[summary]

    Args:
        request ([type]): [description]
        year ([type]): [description]
        month ([type]): [description]
        day ([type]): [description]
        post ([type]): [description]
    """
    post = get_object_or_404(Post, slug=post,status ='published',publish__year = year,
                            publish__month = month, publish__day = day)

    #list of active comments in this post
    comments = post.comments.filter(active=True)
    new_comment = None
    #list of tags in the post
    tags = post.tags.values()
    list_of_tags=[]
    for tag in tags:
        list_of_tags.append(tag['slug'])

    if request.method == 'POST':
        #a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #save comment but no push to db yet
            new_comment = comment_form.save(commit=False)
            #assign the current post to the comment
            new_comment.post=post
            #save comment to db
            new_comment.save()
    else:
        comment_form=CommentForm()
    
    #list of similar posts
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                            .exclude(id=post.id)
    similar_posts =similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request,'blog/post/detail.html',{'post':post,
                                                    'comments':comments,
                                                    'tag':list_of_tags,
                                                    'new_comment':new_comment,
                                                    'comment_form':comment_form,
                                                    'similar_posts':similar_posts})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title','body'),).filter(search=query)
            print(f'query',{query})
            print(f'results: ',{results})
    return render(request,'blog/post/search.html',{'form':form,'query':query,'results':results})