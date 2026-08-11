from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Course, CryptoWallet, CourseAccess


def course_list(request):
    """The /courses/ page -- every published course."""
    courses = Course.objects.filter(is_published=True)
    return render(request, "courses/course_list.html", {"courses": courses})


def course_detail(request, slug):
    """
    A single course's page. What it shows depends on the visitor:
      - not logged in       -> prompt to create an account first
      - logged in, no access -> crypto wallet addresses + payment instructions
      - logged in, has access -> the materials link
    """
    course = get_object_or_404(Course, slug=slug, is_published=True)

    has_access = False
    if request.user.is_authenticated:
        has_access = CourseAccess.objects.filter(user=request.user, course=course).exists()

    wallets = CryptoWallet.objects.filter(is_active=True)

    return render(request, "courses/course_detail.html", {
        "course": course,
        "has_access": has_access,
        "wallets": wallets,
        "payment_email": settings.PAYMENT_CONFIRMATION_EMAIL,
    })


@login_required
def my_courses(request):
    """The logged-in user's own course library -- only courses they've been granted access to."""
    accesses = CourseAccess.objects.filter(user=request.user).select_related("course")
    return render(request, "courses/my_courses.html", {"accesses": accesses})
