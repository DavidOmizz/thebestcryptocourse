from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    A simple grouping for blog posts, e.g. "Basics", "Psychology", "DeFi".
    Shows up as the small tag on each post card.
    """
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=70, unique=True, help_text="Used in the URL, e.g. 'basics'")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    A single blog post. Everything here is editable from /admin/ --
    no need to touch code to publish, edit, or unpublish a post.
    """
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="blog/images/", null=True, blank=True)
    slug = models.SlugField(max_length=220, unique=True, help_text="Used in the URL, e.g. 'reading-a-candlestick-chart'")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    excerpt = models.CharField(
        max_length=280,
        help_text="Short summary shown on the post card (1-2 sentences)."
    )
    body = models.TextField(help_text="Full post content. Plain text or basic HTML.")
    is_published = models.BooleanField(default=True, help_text="Uncheck to hide this post from the site without deleting it.")
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})
