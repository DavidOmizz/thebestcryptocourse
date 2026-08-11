from django.contrib import admin
from .models import Course, Lesson, CryptoWallet, CourseAccess


class LessonInline(admin.TabularInline):
    """Lets you add/edit a course's lessons right on the course's own admin page."""
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "level", "price", "is_published", "order"]
    list_filter = ["is_published", "level"]
    search_fields = ["title", "description"]  # required for autocomplete_fields to work elsewhere
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ["label", "address", "is_active", "order"]
    list_editable = ["is_active", "order"]


@admin.register(CourseAccess)
class CourseAccessAdmin(admin.ModelAdmin):
    """
    This is where you grant access after verifying a payment email.
    Search by the buyer's username/email, pick the course, save -- done.
    """
    list_display = ["user", "course", "granted_at", "note"]
    list_filter = ["course"]
    search_fields = ["user__username", "user__email", "course__title"]
    autocomplete_fields = ["user", "course"]
