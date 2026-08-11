from django.conf import settings
from django.db import models
from django.urls import reverse


class Course(models.Model):
    """
    A single course shown on the site. Buying is handled manually via crypto
    payment: buyers see the wallet addresses from CryptoWallet below, pay,
    then email proof. Once you grant them access (via CourseAccess), the
    `materials_url` link becomes visible to them.
    """
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, help_text="Used in the URL, e.g. 'crypto-trading-fundamentals'")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="beginner")
    description = models.TextField(help_text="Shown on the course card and detail page.")
    lesson_count = models.PositiveIntegerField(default=0, help_text="Shown as '8 lessons'.")
    hours = models.PositiveIntegerField(default=0, help_text="Shown as '4h total'.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="In Naira, e.g. 45000.00")
    materials_url = models.URLField(
        blank=True,
        help_text="Link to the actual course materials (e.g. a private Google Drive folder or "
                   "classroom link). Only shown to users you've granted access to below."
    )
    is_published = models.BooleanField(default=True, help_text="Uncheck to hide this course without deleting it.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first. Use to control display order.")

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"slug": self.slug})


class Lesson(models.Model):
    """
    A single curriculum line shown on the course detail page
    (title + one line of what it covers). This is just the syllabus preview --
    actual lesson delivery happens on Selar once someone buys.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.course.title} -- {self.title}"


class CryptoWallet(models.Model):
    """
    A wallet address shown on a course's "buy" screen. Add one per currency
    you accept (e.g. Bitcoin, USDT). Edit these any time from /admin/ --
    no code change needed.
    """
    label = models.CharField(max_length=60, help_text="e.g. 'Bitcoin (BTC)' or 'USDT (TRC20)'")
    address = models.CharField(max_length=200)
    network_note = models.CharField(
        max_length=200, blank=True,
        help_text="Optional warning shown under the address, e.g. 'TRC20 network only -- other networks will lose funds.'"
    )
    is_active = models.BooleanField(default=True, help_text="Uncheck to stop showing this wallet without deleting it.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["order", "label"]

    def __str__(self):
        return self.label


class CourseAccess(models.Model):
    """
    One row = one user has paid for and been granted one course.
    Created manually from /admin/ after you've verified their payment email.
    Once this exists, that user's course page shows the materials link
    instead of the payment instructions.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_access")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="access_grants")
    granted_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(
        max_length=200, blank=True,
        help_text="Optional, e.g. 'Paid 0.001 BTC, confirmed via email 3 Aug'"
    )

    class Meta:
        unique_together = ("user", "course")
        verbose_name_plural = "Course access grants"

    def __str__(self):
        return f"{self.user} \u2192 {self.course}"
