from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.



class Post(models.Model):
    body=models.TextField()
    slug=models.SlugField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')

    class Meta:
        ordering=('-created',)
     
    def __str__(self):
        return f'{self.slug} - {self.updated}'
    
    def get_absolute_url(self):
       
       return reverse('home:detail', args={self.id , self.slug})
    


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='usercomments')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='postcomments')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='replycomments',blank=True,null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user} - {self.body[:30]}'
    


class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uservotes')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='postvotes')

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'
    
