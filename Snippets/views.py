from django.shortcuts import render , get_object_or_404
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin as Login , UserPassesTestMixin as UserPass
from django.contrib.auth.models import User

def about(request) :
    context = { 
        'posts' : Post.objects.all(), 
        'title' : 'About Author' 
    } 
    return render(request , 'Snippets/about.html' , context)

class PostListView(ListView): 
    model = Post
    template_name = 'Snippets/about.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date'] #Descending order of post
    paginate_by = 5 #Pagination

class UserPostListView(ListView): 
    model = Post
    template_name = 'Snippets/user_post.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5 #Pagination

    def get_queryset(self) : 
            user = get_object_or_404(User , username=self.kwargs.get('username')) #get username from url
            return Post.objects.filter(author=user).order_by('-date')

class PostDetailView(DetailView): 
    model = Post

class PostCreateView(Login , CreateView): 
    model = Post
    fields = ['title' , 'content' , 'img']

    def form_valid(self,form) : 
        form.instance.author = self.request.user #Author for blog post is the current user
        return super().form_valid(form)



class PostUpdateView(Login , UserPass , UpdateView):    
    model = Post
    fields = ['title' , 'content' , 'img']

    def form_valid(self,form) : 
        form.instance.author = self.request.user #Author for blog post is the current user
        return super().form_valid(form)
    
    def test_func(self) : 
        post = self.get_object()
        if self.request.user == post.author : 
            return True 
        else : 
            return False
            
class PostDeleteView(Login , UserPass , DeleteView): 
    model = Post
    success_url = '/'
    def test_func(self) : 
        post = self.get_object()
        if self.request.user == post.author : 
            return True 
        else : 
            return False


def home(request) :

    #Refer the subdirectory within the template directory
    return render(request , 'Snippets/home.html')

def blog(request) : 
    return render(request , 'Snippets/blog.html')