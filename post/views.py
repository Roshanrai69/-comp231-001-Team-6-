from django.shortcuts import render,redirect,get_object_or_404
from django.http import  HttpResponse
from django.views import View
from .models import Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdate, CommentCreateForm,CommentReplyForm, PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Vote
from django.http import JsonResponse
from django.contrib.auth.models import User


class HomeView(LoginRequiredMixin,View):
    form_class = PostSearchForm
    def get(self,request):
        posts = Post.objects.all()
        user = User.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
           
        return render(request, 'post/index.html',{'posts':posts,'search':self.form_class,'user':user})
    




class DetailView(View):

    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id =kwargs['post_id'], slug = kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    def get(self,request,*args,**kwargs):
        comments = self.post_instance.postcomments.filter(is_reply = False)
        # vote = Vote.objects.create(post=self.post_instance, user=request.user)
        return render(request,'post/detail.html',{'post':self.post_instance,'comments':comments,'form':self.form_class,'reply_form':self.form_class_reply})
    # @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid:
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request,'your comment has been submitted successfully','success')
            return redirect('post:detail',self.post_instance.id,self.post_instance.slug)
        

class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        posts = get_object_or_404(Post,id = post_id)
        
        if posts.user.id == request.user.id:
            posts.delete()
            messages.success(request,'Deleted successfully','success')
        else:
            messages.error(request,'Can\'t be deleted','danger')
        return redirect('post:home')
    

class PostUpdateView(View):
    form_class = PostUpdate
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post,id=kwargs['post_id'])

        return super().setup(request, *args, **kwargs)
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        # post = Post.objects.get(id=kwargs['post_id'])
        if not post.user.id == request.user.id:
            messages.error(request,'Can\'t be update','danger')
            return redirect('post:home')
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,post_id):
        post = self.post_instance

        # post = Post.objects.get(id = post_id)
        form = self.form_class(instance = post)
        return render(request,'post/update.html',{'form':form})
    def post(self,request,post_id):
        post = self.post_instance

    #   post = Post.objects.get(id = post_id)
        form = self.form_class(request.POST,instance=post)
        if form.is_valid:
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request,'updated successfully','success')
            return redirect('post:detail',post.id,post.slug)

# class PostCreateView(LoginRequiredMixin,View):
#     form_class = PostUpdate
#     def get(self,request,*args,**kwargs):
#         form = self.form_class
#         return(request,'post/create.html',{'form':form})
#     def post(self,request,*args,**kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid:
#             new_post = form.save(commit=False)
#             new_post.slug = slugify(form.cleaned_data['body'][:30])
#             new_post.user = request.user
#             new_post.save()
#             messages.success(request,'Post created','success')
#             return redirect('post:detail',new_post.id, new_post.slug) 
        
def create_post(request):
    if request.method == 'POST':
        form = PostUpdate(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            return redirect('post:detail',new_post.id, new_post.slug)
    else:
        form = PostUpdate()
    return render(request, 'post/create.html', {'form': form,"section":"text-post"})





class ReplyCommentView(LoginRequiredMixin,View):
    form_class = CommentReplyForm
    def post(self,request,post_id,comment_id):
         post = get_object_or_404(Post,id = post_id)
         comment = get_object_or_404(Comment,id = comment_id)
         form = self.form_class(request.POST)
         if form.is_valid():
            reply = form.save(commit = False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request,'you replied sucessfully','success')
         return redirect('post:detail', post.id, post.slug)




# class PostLikeView(LoginRequiredMixin,View):
#     def get(self,request,post_id):
#         post = get_object_or_404(Post,id = post_id)
#         like = Vote.objects.filter(post = post,user = request.user)
#         if like.exists():
#             vote = "dislike"
#         else:
#             Vote.objects.create(post = post,user = request.user)
#             vote = "like"
#         return redirect('post:detail', post.id, post.slug)







def post_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        if Vote.objects.filter(post=post, user=request.user).exists():
            return JsonResponse({'status': 'error', 'message': 'You have already liked this post.'})
        Vote.objects.create(post=post, user=request.user)
        likes_count = Vote.objects.filter(post=post).count()
        return JsonResponse({'status': 'success', 'likes_count': likes_count})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})