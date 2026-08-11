from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from blog.models import Post
from courses.models import Course
from .forms import RegisterForm


def home(request):
    """The homepage -- hero, then latest 3 posts, then all courses."""
    latest_posts = Post.objects.filter(is_published=True)[:3]
    courses = Course.objects.filter(is_published=True)
    return render(request, "core/home.html", {
        "latest_posts": latest_posts,
        "courses": courses,
    })


def register(request):
    """
    A simple sign-up form. On success, logs the user in immediately and
    sends them back to wherever they were trying to go (e.g. back to the
    course page they wanted to buy) via the `next` parameter.
    """
    next_url = request.POST.get("next") or request.GET.get("next") or "core:home"

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(next_url)
    else:
        form = RegisterForm()

    return render(request, "core/register.html", {"form": form, "next": next_url})
