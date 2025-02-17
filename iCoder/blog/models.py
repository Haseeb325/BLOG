from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno =models.AutoField(primary_key=True)
    title= models.CharField(max_length=255)
    content = models.CharField(max_length=12000)
    author = models.CharField(max_length=100)
    slug = models.CharField(max_length=130)
    timeStamp =models.DateTimeField( blank=True)
    
    def __str__(self) -> str:
        return self.title + 'by' + self.author



class BlogComment(models.Model):

    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    parent = models.ForeignKey('self' , on_delete=models.CASCADE , null=True , blank=True) # apne ap pr he foreignkey banani hoti hai to self likht hain
    timeStamp = models.DateTimeField(default=now)
   
    def __str__(self):
        return self.comment[:50] + "... by " + self.user.username
