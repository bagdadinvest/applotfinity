# lotfinity website

Code for site at: http://hello-from.lotfinity.tech


## Getting started

Make sure a recent version of Python is installed on your system.
Open this directory in a command prompt, then:

1. Install the software:
   ```
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```
   python manage.py runserver
   ```

3. Go to http://localhost:8000/ in your browser, or http://localhost:8000/admin/
   to log in and get to work!

## Documentation links

* To customize the content, design, and features of the site see
  [Wagtail CRX](https://docs.coderedcorp.com/wagtail-crx/).

* For deeper customization of backend code see
  [Wagtail](http://docs.wagtail.io/) and
  [Django](https://docs.djangoproject.com/).

* For HTML template design see [Bootstrap](https://getbootstrap.com/).

---

Made with ♥ using [Wagtail](https://wagtail.io/) +
[CodeRed Extensions](https://www.coderedcorp.com/cms/)

## Static site export

There are two ways to produce a static version of this site.

- Built-in (no new dependency):
  - Run: `python manage.py buildstatic` (outputs to `build/`).
  - Options: `--build-dir <path>`, `--skip-static`, `--skip-media`.
  - This renders every live public Wagtail page and copies `static/` and `media/` into the build.

- Wagtail‑Bakery (recommended when you can install packages):
  1. Install: `pip install wagtail-bakery`.
  2. Add to `INSTALLED_APPS`: `'bakery', 'wagtailbakery'`.
  3. In `mysite/settings/base.py`, add:
     - `BUILD_DIR = BASE_DIR / 'build'`
     - `BAKERY_VIEWS = ('wagtailbakery.views.AllPagesView',)`
  4. Build: `python manage.py build` (outputs to `build/`).

Notes:
- Forms, search, and AJAX-only features won’t work on a static host unless replaced with client-side or third‑party services.
- Ensure media files are safe to publish before copying `media/` to the static host.
