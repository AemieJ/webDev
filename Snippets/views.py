from django.shortcuts import render , get_object_or_404
from django.db.models import Q , F , Count
from django.http import JsonResponse , HttpResponse
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView , RedirectView
from .models import Post , Like , ViewPost
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin as Login , UserPassesTestMixin as UserPass
from django.contrib.auth.models import User

#Managing data for the model system
username = []
post = []
ip = []

def counter( username , post , current_user , current_post) : 
    count = 0
    data = []
    length = len(username) 
    for sample in range(length) : 
        if current_user == username[sample] :
            data.append(post[sample]) 
    
    for title in data : 
        if current_post == title : 
            count += 1
    return count

def like(request):
    if not request.user.is_authenticated : 
        messages.info(request , 'User needs to be logged in to like the blog.')

    if request.user.is_authenticated :
        if request.method == 'GET':
            post_id = request.GET['post_id']
            likedpost = Post.objects.get(id = post_id)
            m = Like( post=likedpost )
            m.save() 
            user = request.user.username 
            username.append(user)
            post.append(likedpost)
            count = counter(username , post , user , likedpost)  
            list_postId = Like.objects.all().values('post')          
            for ids in list_postId :  
                    if post_id == str(ids['post']) and count == 1 :
                        m.count_like += 1
            if m.count_like != 0:
                m.save()
            if m.count_like == 0:
                m.delete()

            print(Like.objects.values('default_count').distinct())

            return HttpResponse('success')
        else:
            return HttpResponse("unsuccesful")

def counterIp(ip , current_ip) : 
    count = 0 
    for ip_addr in ip : 
        if current_ip == ip_addr : 
            count += 1 
    return count

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def view(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        view_post = Post.objects.get(id = post_id)
        v = ViewPost( post=view_post )
        v.save() 
        
        ip_addr = get_client_ip(request)
        ip.append(ip_addr)
        count = counterIp(ip , ip_addr) 
        view_postId = ViewPost.objects.all().values('post')
        for ids in view_postId :  
                if post_id == str(ids['post']): 
                    v.count_views += 1
        if v.count_views != 0:  
            v.save()
        if v.count_views == 0:
           v.delete() 

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
    template_name = 'Snippets/blog.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date'] #Descending order of post
    paginate_by = 5 #Pagination
    queryset = Post.objects.all()

    def get_context_data(self ,**kwargs) :
        context = super(PostListView,self).get_context_data(**kwargs)
        context['likes'] = Like.objects.values('post').annotate(post_count=Count('post')).filter(post_count__gt=1)
        context['views'] = ViewPost.objects.values('post').annotate(post_view=Count('post')).filter(post_view__gt=1)
        return context

class UserPostListView(ListView): 
    model = Post
    template_name = 'Snippets/user_post.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5 #Pagination
    queryset = Post.objects.all()

    def get_queryset(self) : 
            user = get_object_or_404(User , username=self.kwargs.get('username')) #get username from url
            return Post.objects.filter(author=user).order_by('-date')

    def get_context_data(self ,**kwargs) :
        context = super(UserPostListView,self).get_context_data(**kwargs)
        context['likes'] = Like.objects.values('post').annotate(post_count=Count('post')).filter(post_count__gt=1)
        context['views'] = ViewPost.objects.values('post').annotate(post_view=Count('post')).filter(post_view__gt=1)
        return context

class SearchPostListView(ListView) : 
    model = Post
    template_name = 'Snippets/search_post.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5 #Pagination
    queryset = Post.objects.all()

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-date')
        else : 
            posts = Post.objects.all().order_by('-date')
        return posts
    
    def get_context_data(self ,**kwargs) :
        context = super(SearchPostListView,self).get_context_data(**kwargs)
        context['likes'] = Like.objects.values('post').annotate(post_count=Count('post')).filter(post_count__gt=1)
        context['views'] = ViewPost.objects.values('post').annotate(post_view=Count('post')).filter(post_view__gt=1)
        return context

class PostDetailView(DetailView): 
    model = Post
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self ,**kwargs) :
        context = super(PostDetailView,self).get_context_data(**kwargs)
        context['likes'] = Like.objects.values('post').annotate(post_count=Count('post')).filter(post_count__gt=1)
        context['defaultLike'] = Like.objects.values('default_count').distinct()
        context['views'] = ViewPost.objects.values('post').annotate(post_view=Count('post')).filter(post_view__gt=1)
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

#Problem Faced : Unable to delete the post.
class PostDeleteView(Login , UserPass , DeleteView): 
    model = Post
    success_url ='/'

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