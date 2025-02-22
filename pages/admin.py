from django.contrib import admin
from .models import BlogPost,NewUsers
# Register your models here.

admin.site.register(BlogPost)

class Project(admin.ModelAdmin):
    list_display=['username','email','password']


admin.site.register(NewUsers,Project)