"""
Pages Web Urls
"""

# Standard library imports.
from django.urls import path

# Related third party imports.

# Local application/library specific imports.
from pages.views.web import views

urlpatterns = (
    path('detail/<int:pk>/', views.PageDetailView.as_view()),
)
