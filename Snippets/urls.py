from django.urls import path 
from .views import PostListView , PostDetailView , PostCreateView , PostUpdateView , PostDeleteView , UserPostListView
from . import views 

urlpatterns = [
    #This sets the path to the home page which displays everything in the function home
    path('',views.home , name = 'Snippets'),
    path('about/',PostListView.as_view(), name = 'About'),
    path('user/<str:username>',UserPostListView.as_view(), name = 'user-posts'),
    path('post/<int:pk>/',PostDetailView.as_view(), name = 'post-detail'), #pk decides which blog to open based on id
    path('post/new/',PostCreateView.as_view(), name = 'post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(), name = 'post-delete'),
    path('blog/',views.blog , name = 'Blogs'),
]