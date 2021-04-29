from django.urls import path
from .import views
import blog

app_name = blog

urlpatterns = [
    path('',views.post_list,name = 'post_list'),
    path('<int:year>/<int:month>/<int:day>/<string:slug>',views.post_detail,name = 'post_detail')

]