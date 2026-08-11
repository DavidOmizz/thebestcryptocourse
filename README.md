# TheBestCryptoCourse — Django site

Blog + course showcase, admin-managed, with a manual crypto payment flow:
buyers register an account, see a wallet address on the course page, pay,
then email proof. You (admin) verify the payment and grant access from
/admin/ — the buyer's course page then unlocks the materials link.

## Project layout (what each folder does)

```
thebestcryptocourse/
├── config/          Project settings, main urls.py — the "control room"
├── core/             Homepage view + site-wide template helpers
├── blog/             Blog posts & categories (model, admin, views, templates)
├── courses/          Courses & lessons (model, admin, views, templates)
├── templates/         base.html — the shared header/footer/nav every page uses
├── static/css/        style.css — all the site's design in one file
└── seed.py            Sample content loader (optional, for testing)
```

Each app (`blog`, `courses`, `core`) follows the same 4 files:
- `models.py` — what data looks like (a blog post, a course)
- `admin.py` — what you see/edit in the /admin/ panel
- `views.py` — what happens when someone visits a page (fetch data, show a template)
- `urls.py` — which URL maps to which view
- `templates/<app_name>/*.html` — what the page actually looks like

## Running it locally

```bash
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate                       # sets up the database
python manage.py shell < seed.py                # loads sample blog posts & courses (optional)
python manage.py createsuperuser                # creates your admin login
python manage.py runserver
```

Then visit:
- **http://127.0.0.1:8000/** — the site
- **http://127.0.0.1:8000/admin/** — the admin panel (log in with the superuser you just created)

## How to edit content (this is the part your client will actually use)

Everything below is done through `/admin/` in a browser — no code editing needed:

- **Add/edit a blog post** → Admin → Blog → Posts → Add Post. Fill in title, excerpt,
  body, pick a category. Uncheck "is published" to hide a post without deleting it.
- **Add/edit a course** → Admin → Courses → Courses → Add Course. Fill in title,
  level, description, price, lesson count/hours. Add `materials_url` (e.g. a
  private Google Drive folder link) — this only becomes visible to a buyer once
  you've granted them access (see below).
- **Add lessons to a course's curriculum** → open the course in admin, scroll down —
  there's a "Lessons" section right on the same page to add curriculum lines.
- **Reorder courses** → change the `order` number (lower = shows first).
- **Edit your crypto wallet addresses** → Admin → Courses → Crypto wallets.
  Add one row per currency you accept (e.g. Bitcoin, USDT). Uncheck "is active"
  to temporarily stop showing one without deleting it.
- **Grant a buyer access after payment** → Admin → Courses → Course access grants →
  Add. Search for the buyer by username or email (they'll have given you this in
  their payment confirmation email), pick the course, save. Their course page
  unlocks the materials link immediately the next time they load it.
- **Change where payment confirmation emails should be sent** → set the
  `PAYMENT_CONFIRMATION_EMAIL` environment variable (defaults to
  `payments@thebestcryptocourse.com` if unset).

## How to edit the design

- All colors, fonts, spacing live in `static/css/style.css` as CSS variables at the
  top of the file (`--bg`, `--mint`, `--text`, etc.) — change a value there and it
  updates everywhere.
- Page structure/layout lives in the `.html` files under each app's `templates/`
  folder, plus `templates/base.html` for the shared header/nav/footer.
- The site name shown in the header is set once, in `config/settings.py`
  (`SITE_NAME`) or via the `SITE_NAME` environment variable in production —
  no need to edit templates to rename the brand.

## Deploying to Railway

This project does **not** need to touch the existing WordPress hosting at all —
it deploys somewhere new, and only the domain's DNS gets pointed at it.

1. Push this project to a GitHub repo.
2. On Railway: New Project → Deploy from GitHub repo → select this repo.
3. Add a PostgreSQL database to the project (Railway sets `DATABASE_URL`
   automatically — you don't need to configure it).
4. Under your web service's Variables tab, set:
   - `SECRET_KEY` — any long random string
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — `thebestcryptocourse.com,www.thebestcryptocourse.com,<your-railway-domain>`
   - `SITE_NAME` — `TheBestCryptoCourse`
5. Railway runs `release: python manage.py migrate` automatically before each
   deploy (see `Procfile`), so the database schema stays up to date.
6. Once it's live on Railway's own `*.up.railway.app` URL, go to your domain
   registrar's DNS settings and point the domain at Railway (Railway's
   dashboard shows you the exact CNAME/A record to add — Settings → Networking
   → Custom Domain). The old WordPress hosting is no longer involved once
   this DNS change takes effect.
7. Run `python manage.py createsuperuser` once against production (Railway's
   dashboard has a "Run a command" / shell option) so you have an admin login
   on the live site too.

## What's deliberately manual (by design, not a limitation)

- **No automated payment processing.** There's no blockchain listener checking
  whether a wallet address actually received funds — that's a meaningfully
  bigger (and riskier) build. Instead, buyers self-report payment by email,
  and access is granted by a human after checking it. This is standard for
  small crypto-accepting sellers and keeps the system simple and auditable
  (every grant in Course Access shows who granted it and when).
- **No automatic "instant unlock."** There will always be a manual step
  between payment and access. If volume grows enough that this becomes a
  bottleneck, a payment processor (e.g. NOWPayments, Coinbase Commerce) can
  be integrated later to automate the verification step — the account/access
  system already in place wouldn't need to change, only the payment step
  would move from manual to automatic.
