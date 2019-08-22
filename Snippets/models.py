from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User #The users dealing with the website
from django.urls import reverse

from PIL import Image 

#Creating the databases
class Post(models.Model) : 
    title = models.CharField(max_length=100) 
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User , on_delete=models.CASCADE) #If user deleted , delete their posts
    img = models.ImageField(default='post_pics/default.jpg' , upload_to="post_pics")


    def __str__(self) : 
        #What we want our database instance to print
        return self.title 

    def save(self , *args , **kwargs) : 
        super().save(*args,**kwargs) 

        img = Image.open(self.img.path)
        img.save(self.img.path)

    #Provide reverse which returns a string rather than redirecting
    def get_absolute_url(self) : 
        return reverse('post-detail', kwargs={'pk':self.pk})


#Migrations helps in updation of our sql databases.
