import os
import shutil
from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.test import Client

from wagtail.models import Page


class Command(BaseCommand):
    help = "Build a static export of all live Wagtail pages into a build directory."

    def add_arguments(self, parser):
        parser.add_argument(
            "--build-dir",
            default=str(Path(settings.BASE_DIR) / "build"),
            help="Output directory for the static site (default: BASE_DIR/build)",
        )
        parser.add_argument(
            "--skip-static",
            action="store_true",
            help="Do not run collectstatic/copy static files.",
        )
        parser.add_argument(
            "--skip-media",
            action="store_true",
            help="Do not copy media files.",
        )

    def handle(self, *args, **options):
        build_dir = Path(options["build_dir"]).resolve()
        self.stdout.write(self.style.NOTICE(f"Building static site to: {build_dir}"))

        # Prepare build directory
        if build_dir.exists():
            self.stdout.write("Cleaning existing build directory...")
            shutil.rmtree(build_dir)
        build_dir.mkdir(parents=True, exist_ok=True)

        # Collect static files
        if not options["skip_static"]:
            self.stdout.write("Collecting static files...")
            call_command("collectstatic", interactive=False, verbosity=0)
            static_root = Path(settings.STATIC_ROOT)
            if static_root.exists():
                shutil.copytree(static_root, build_dir / "static")

        # Copy media files (best-effort)
        if not options["skip_media"]:
            media_root = Path(settings.MEDIA_ROOT)
            if media_root.exists():
                self.stdout.write("Copying media files...")
                shutil.copytree(media_root, build_dir / "media")

        client = Client()

        # Iterate over all live, public pages across all sites
        pages = (
            Page.objects.live()
            .public()
            .specific()
            .defer_streamfields()
            .order_by("path")
        )

        total = pages.count()
        self.stdout.write(self.style.NOTICE(f"Rendering {total} pages..."))

        for page in pages.iterator():
            parts = page.get_url_parts()
            if not parts:
                # Page not routable (no site)
                continue

            site_id, root_url, page_path = parts
            parsed = urlparse(root_url)
            host = parsed.netloc

            # Ensure path starts with '/'
            path = page_path if page_path.startswith("/") else f"/{page_path}"

            try:
                response = client.get(path, HTTP_HOST=host)
            except Exception as exc:
                self.stdout.write(self.style.WARNING(f"Failed to GET {path}: {exc}"))
                continue

            if response.status_code != 200:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping {path} (status {response.status_code})"
                    )
                )
                continue

            # Determine output file path (directory/index.html)
            out_dir = build_dir / path.strip("/")
            if not str(path).endswith("/"):
                # Treat non-slash as directory style too (e.g., /about -> /about/index.html)
                out_dir = build_dir / path.strip("/")
            if str(out_dir) == str(build_dir):
                # Root path
                out_dir = build_dir
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / "index.html"

            with open(out_file, "wb") as f:
                f.write(response.content)

            self.stdout.write(f"Rendered {path} -> {out_file.relative_to(build_dir)}")

        self.stdout.write(self.style.SUCCESS(f"Static build complete: {build_dir}"))

