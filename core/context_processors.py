from django.conf import settings

# Static ticker content for the scrolling bar at the very top of the site.
# Format: (label, change_text, direction) -- direction is "up", "down", or "" for plain text.
# This is intentionally not database-backed to keep Phase 1 simple; if you
# want this editable from /admin/ later, it can become a small model.
TICKER_ITEMS = [
    ("BTC", "\u25B2 2.4%", "up"),
    ("ETH", "\u25B2 1.1%", "up"),
    ("New lesson published: \"Reading Order Books\"", "", ""),
    ("SOL", "\u25BC 0.8%", "down"),
    ("12 traders started \"Technical Analysis Masterclass\" this week", "", ""),
]


def site_settings(request):
    """Makes {{ site_name }} and {{ ticker_items }} available in every template."""
    return {
        "site_name": settings.SITE_NAME,
        "ticker_items": TICKER_ITEMS,
    }
