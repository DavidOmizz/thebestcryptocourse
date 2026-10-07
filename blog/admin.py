from django.contrib import admin
from .models import Category, Post

admin.site.site_header = "The Best Crypto Course"
admin.site.site_title = "The Best Crypto Course Admin"
admin.site.index_title = "Manage Your Website"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}  # auto-fills the slug as you type the name


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "is_published", "published_at"]
    list_filter = ["is_published", "category"]
    search_fields = ["title", "excerpt", "body"]
    prepopulated_fields = {"slug": ("title",)}
