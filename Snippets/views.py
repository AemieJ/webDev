from django.shortcuts import render , get_object_or_404
from django.db.models import Q , F
from django.http import JsonResponse , HttpResponse
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView , RedirectView
from .models import Post , Like
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin as Login , UserPassesTestMixin as UserPass
from django.contrib.auth.models import User

@login_required
def like(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        likedpost = Post.objects.get(id = post_id)
        m = Like( post=likedpost )
        m.save() 
        
        list_postId = Like.objects.all().values('post')
        for ids in list_postId :  
                if post_id == str(ids['post']) : 
                    m.count_like += 1
        m.save()
        return HttpResponse('success')
    else:
        return HttpResponse("unsuccesful")

def about(request) :
    context = { 
        'posts' : Post.objects.all(), 
        'title' : 'Blogs' 
    } 
    return render(request , 'Snippets/blog.html' , context)

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

class SearchPostListView(ListView) : 
    model = Post
    template_name = 'Snippets/search_post.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5 #Pagination

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-date')
        else : 
            posts = Post.objects.all().order_by('-date')
        return posts

class PostDetailView(DetailView): 
    model = Post
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self ,**kwargs) :
        context = super(PostDetailView,self).get_context_data(**kwargs)
        context['likes'] = Like.objects.all().order_by('-count_like')
        return context

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
    first_post = Post.objects.all().order_by('-date')[0]
    second_post = Post.objects.all().order_by('-date')[1]
    third_post = Post.objects.all().order_by('-date')[2]
    context = {
        'first'  : first_post , 
        'second' : second_post , 
        'third'  : third_post

    }
    return render(request , 'Snippets/home.html' , context)

def blog(request) : 
    return render(request , 'Snippets/blog.html')