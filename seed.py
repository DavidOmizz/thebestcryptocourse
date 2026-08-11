"""
Loads the same sample content that was in the HTML demo, so the site
looks populated right away. Run once with: python manage.py shell < seed.py
Safe to re-run -- it won't create duplicates.
"""
import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from blog.models import Category, Post
from courses.models import Course, Lesson, CryptoWallet

basics, _ = Category.objects.get_or_create(name="Basics", slug="basics")
psychology, _ = Category.objects.get_or_create(name="Psychology", slug="psychology")
defi_cat, _ = Category.objects.get_or_create(name="DeFi", slug="defi")

Post.objects.get_or_create(
    slug="reading-a-candlestick-chart",
    defaults=dict(
        title="Reading a Candlestick Chart in Under 5 Minutes",
        category=basics,
        excerpt="The four numbers behind every candle, and what they're actually telling you.",
        body="Every candlestick tells you four numbers: open, high, low, and close, for whatever "
             "time period you're looking at. Once you can read those four numbers at a glance, "
             "the rest of technical analysis starts to make a lot more sense...",
    ),
)
Post.objects.get_or_create(
    slug="buy-the-dip",
    defaults=dict(
        title="What Actually Happens When You 'Buy the Dip'",
        category=psychology,
        excerpt="A calmer look at one of the most repeated — and misunderstood — phrases in trading.",
        body="\"Buy the dip\" sounds simple until you're actually staring at a falling chart wondering "
             "if it's a dip or the start of something much worse. Here's how to tell the difference...",
    ),
)
Post.objects.get_or_create(
    slug="defi-explained",
    defaults=dict(
        title="DeFi, Explained Without the Jargon",
        category=defi_cat,
        excerpt="Lending pools, liquidity, and yield — in plain language, no whitepaper required.",
        body="DeFi just means financial services -- lending, borrowing, trading -- built with code "
             "instead of a bank behind the counter. Here's what that actually looks like in practice...",
    ),
)

c1, _ = Course.objects.get_or_create(
    slug="crypto-trading-fundamentals",
    defaults=dict(
        title="Crypto Trading Fundamentals", level="beginner",
        description="Wallets, exchanges, order types, and how to read the market before risking anything.",
        lesson_count=8, hours=4, price=45000, order=1,
    ),
)
if not c1.lessons.exists():
    Lesson.objects.create(course=c1, order=1, title="Setting up a wallet safely",
        summary="Custodial vs. non-custodial wallets, and the habits that prevent most beginner mistakes.")
    Lesson.objects.create(course=c1, order=2, title="Market, limit, and stop orders",
        summary="What each order type does, and when to reach for one over another.")
    Lesson.objects.create(course=c1, order=3, title="Reading your first order book",
        summary="Bids, asks, and spread — telling a calm market from one about to move.")

c2, _ = Course.objects.get_or_create(
    slug="technical-analysis-masterclass",
    defaults=dict(
        title="Technical Analysis Masterclass", level="intermediate",
        description="Chart patterns, indicators, and a repeatable process for spotting setups.",
        lesson_count=14, hours=7, price=85000, order=2,
    ),
)
if not c2.lessons.exists():
    Lesson.objects.create(course=c2, order=1, title="Support, resistance & trendlines",
        summary="The three lines every chart is built on, and how to draw them without fooling yourself.")
    Lesson.objects.create(course=c2, order=2, title="Moving averages in practice",
        summary="Using the 50/200 crossover and EMAs to read momentum.")
    Lesson.objects.create(course=c2, order=3, title="Building a setup checklist",
        summary="A short, repeatable checklist you run before every trade.")

c3, _ = Course.objects.get_or_create(
    slug="defi-yield-strategies",
    defaults=dict(
        title="DeFi & Yield Strategies", level="advanced",
        description="Liquidity provision, lending markets, and evaluating real risk versus real yield.",
        lesson_count=11, hours=6, price=120000, order=3,
    ),
)
if not c3.lessons.exists():
    Lesson.objects.create(course=c3, order=1, title="How liquidity pools price risk",
        summary="Impermanent loss, explained with real numbers.")
    Lesson.objects.create(course=c3, order=2, title="Evaluating a lending protocol",
        summary="A short framework for judging whether a yield is sustainable.")
    Lesson.objects.create(course=c3, order=3, title="Building a small, diversified position",
        summary="Sizing a first DeFi allocation like any other portfolio risk.")

CryptoWallet.objects.get_or_create(
    label="Bitcoin (BTC)",
    defaults=dict(address="bc1qxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", order=1),
)
CryptoWallet.objects.get_or_create(
    label="USDT (TRC20)",
    defaults=dict(
        address="TXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        network_note="TRC20 network only -- sending on another network will lose funds.",
        order=2,
    ),
)

print("Seed complete:", Post.objects.count(), "posts,", Course.objects.count(), "courses,", CryptoWallet.objects.count(), "wallets.")
