from django.contrib import admin
from .models import Post , Like , ViewPost

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(ViewPost)