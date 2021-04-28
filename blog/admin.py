"""Admin models only 
"""

from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """[summary]

    Args:
        admin ([type]): [description]

    Vars:
        
    """
    list_display=('title','slug','author','likes','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title','body','authors')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status','likes','publish')
