from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=20)
    slug = models.SlugField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    views = models.IntegerField(default=0) #baxis sayi
    
    tags = TaggableManager()
    def update_views(self, *args, **kwargs):  #baxis sayisi
        self.views = self.views + 1
        super(Post, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

    

    


class Exam(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    qroup = models.IntegerField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name



class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    name=models.CharField(max_length=50)
    email=models.EmailField()
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)