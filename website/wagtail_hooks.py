from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.panels import FieldPanel
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import TechStack


class TechStackSnippetViewSet(SnippetViewSet):
    model = TechStack
    ordering = ("name",)
    search_fields = ("name",)
    icon = "tag"
    inspect_view_enabled = True
    panels = [
        FieldPanel("name"),
    ]

class AppsSnippetGroup(SnippetViewSetGroup):
    menu_label = "Apps"
    menu_icon = "folder-open-inverse"
    menu_order = 200
    items = (
        TechStackSnippetViewSet,
    )

