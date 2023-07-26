from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import PostForm, CommentForm
from .models import Post, Category, Comment, User
from .utils import paginator_page, select_posts, get_user_posts


class UserEditView(UpdateView):
    model = User
    template_name = 'blog/profile_edit.html'
    fields = ['first_name', 'last_name', 'username', 'email']

    def get_success_url(self) -> str:
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.get_object().username})

    def get_object(self) -> User:
        return self.request.user


def index(request):
    post_list = select_posts(Post.objects)
    page_obj = paginator_page(request, post_list)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        post = get_object_or_404(Post.objects.filter(is_published=True), pk=pk)

    form = CommentForm(request.POST)
    comments = post.comments.all()
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug,)
    post_list = select_posts(category.posts)
    page_obj = paginator_page(request, post_list)
    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, 'blog/category.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = get_user_posts(request.user, username)
    page_obj = paginator_page(request, posts)
    context = {
        'author': author,
        'page_obj': page_obj
    }
    return render(request, 'blog/profile.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None)
    context = {
        'form': form
    }
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user)
    return render(request, 'blog/create.html', context)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, instance=post)
    if post.author != request.user:
        return redirect('blog:post_detail', pk)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk)
    context = {
        'form': form
    }
    return render(request, 'blog/create.html', context)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=post)
    context = {'form': form}
    if post.author != request.user:
        return redirect('blog:post_detail', pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', post.author)
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    form = CommentForm(request.POST or None, instance=comment)
    context = {
        'comment': comment,
        'form': form
    }
    if comment.author != request.user:
        return redirect('blog:post_detail', pk)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    context = {
        'comment': comment,
    }
    if comment.author != request.user:
        return redirect('blog:post_detail', pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk)
    return render(request, 'blog/comment.html', context)
