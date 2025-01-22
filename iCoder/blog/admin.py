from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Post)
# admin.site.register((Post , BlogComment))  # aise b kr skte hain
admin.site.register(BlogComment)
