"""
Create or customize your page models here.
"""

from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedWebPage
from modelcluster.fields import ParentalKey


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"


class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["website.EventIndexPage"]
    template = "coderedcms/pages/event_page.html"


class EventIndexPage(CoderedEventIndexPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "website.EventPage"

    # Only allow EventPages beneath this page.
    subpage_types = ["website.EventPage"]

    template = "coderedcms/pages/event_index_page.html"


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class LocationPage(CoderedLocationPage):
    """
    A page that holds a location.  This could be a store, a restaurant, etc.
    """

    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["website.LocationIndexPage"]


class LocationIndexPage(CoderedLocationIndexPage):
    """
    A page that holds a list of locations and displays them with a Google Map.
    This does require a Google Maps API Key in Settings > CRX Settings
    """

    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"


from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from django.db import models

@register_snippet
class TechStack(models.Model):
    """
    Represents a reusable technology or tool that can be associated with apps.
    """
    name = models.CharField(max_length=255, verbose_name="Technology Name")
    description = models.TextField(blank=True, verbose_name="Description")
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Logo"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("logo"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tech Stack"
        verbose_name_plural = "Tech Stacks"

from wagtail.blocks import RichTextBlock, StructBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock

class AppStreamBlock(StreamBlock):
    heading = RichTextBlock(
        features=["h2", "h3", "bold", "italic"], 
        icon="title", 
        label="Heading"
    )
    paragraph = RichTextBlock(icon="pilcrow", label="Paragraph")
    image = ImageChooserBlock(icon="image", label="Image")

    class Meta:
        icon = "placeholder"
        label = "App Content Blocks"

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.fields import ImageField
from modelcluster.fields import ParentalManyToManyField
from django import forms

class AppPage(Page):
    """
    A page representing an individual app.
    """
    mockup_design = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Mockup Design",
    )
    description = models.TextField(blank=True, verbose_name="App Description")
    tech_stack = ParentalManyToManyField("TechStack", blank=True)

    body = StreamField(
        AppStreamBlock(),  # Use the custom block defined earlier
        verbose_name="Page Body",
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("mockup_design"),
        FieldPanel("description"),
        FieldPanel("tech_stack", widget=forms.CheckboxSelectMultiple),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "App Page"

class AppsIndexPage(Page):
    """
    An index page listing all apps.
    """
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="An image to represent this page.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
    ]

    # Restrict subpages to only AppPage
    subpage_types = ["AppPage"]

    def get_apps(self):
        return AppPage.objects.live().descendant_of(self).order_by("-first_published_at")

    def get_context(self, request):
        context = super().get_context(request)
        apps = self.get_apps()
        context["apps"] = apps
        return context
