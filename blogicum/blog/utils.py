from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils import timezone as tz

from .constants import COUNT_PUBLICATIONS_ON_PAGE
from .models import Post, User


def paginator_page(request, posts):
    paginator = Paginator(posts, COUNT_PUBLICATIONS_ON_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def select_posts(posts):
    return posts.select_related(
        'location',
        'author',
        'category'
    ).filter(
        is_published=True,
        pub_date__lt=datetime.now(),
        category__is_published=True
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')


def get_user_posts(
    request_user: User,
    username: str
) -> QuerySet[Post]:
    posts = Post.objects.select_related(
        'category',
        'location',
        'author',
    ).filter(
        author__username=username,
    )
    if username != request_user.username:
        posts = posts.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=tz.now(),
        )
    posts = posts.annotate(comment_count=Count('comments')).order_by(
        '-pub_date'
    )
    return posts
