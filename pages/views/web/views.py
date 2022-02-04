"""
Pages Web Views
"""

# Standard library imports.

# Related third party imports.
from django.views.generic.detail import DetailView

# Local application/library specific imports.
from pages.models import Page


class PageDetailView(DetailView):
    """
    Endpoint to open page details view.
    """
    model = Page
    context_object_name = 'page'
    template_name = 'pages/detail_view.html'
