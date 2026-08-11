from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    """The /blog/ page -- every published post, newest first."""
    posts = Post.objects.filter(is_published=True)
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, slug):
    """A single post's page, e.g. /blog/reading-a-candlestick-chart/"""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "blog/post_detail.html", {"post": post})
