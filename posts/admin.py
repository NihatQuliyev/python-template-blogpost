from django.contrib import admin

from .models import Author, Category, Post , Exam , Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Exam)
admin.site.register(Comment)
