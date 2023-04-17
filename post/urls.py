from django.urls import path
from . import views
app_name = "post"


urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('post/<int:post_id>/<slug:post_slug>/',views.DetailView.as_view(),name='detail'),
    path('post/delete/<int:post_id>',views.PostDeleteView.as_view(),name='post_delete'),
    path('post/update/<int:post_id>',views.PostUpdateView.as_view(),name='post_update'),
    # path('post/create/',views.PostCreateView.as_view(),name='post_create'),
    path('post/create/',views.create_post,name='post_create'),
    path('reply/<int:post_id>/<int:comment_id>/',views.ReplyCommentView.as_view(),name="reply_comment"),
    # path('like/<int:post_id>/',views.PostLikeView.as_view(),name="post_like"),
    path('like/<int:post_id>/',views.post_like,name="post_like")
   
]