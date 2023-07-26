from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('category/<slug:category_slug>/',
         views.category_posts,
         name='category_posts'),
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('user/',
         login_required(views.UserEditView.as_view()),
         name='edit_profile'),
    path('posts/<int:pk>/',
         views.post_detail,
         name='post_detail'),
    path('posts/create/', views.post_create, name='create_post'),
    path('posts/<int:pk>/edit/', views.post_edit, name='edit_post'),
    path('posts/<int:pk>/delete/', views.post_delete, name='delete_post'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:pk>/edit_comment/<int:comment_pk>/',
         views.edit_comment,
         name='edit_comment'),
    path('posts/<int:pk>/delete_comment/<int:comment_pk>/',
         views.delete_comment,
         name='delete_comment'),
]
