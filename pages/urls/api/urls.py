"""
Pages API Urls
"""

# Standard library imports.
from django.urls import path

# Related third party imports.

# Local application/library specific imports.
from pages.views.api import views

urlpatterns = (
    path('detail/<int:page_id>/', views.PageDetailAPIView.as_view()),
    path('detail/<int:page_id>/version/<int:version_id>/', views.PageDetailVersionAPIView.as_view()),
    path('list/', views.PagesListAPIView.as_view()),
    path('versions_list/<int:page_id>/', views.PageVersionsListAPIView.as_view()),
    path('update/<int:page_id>/', views.PageUpdateAPIView.as_view()),
    path('reverse/<int:page_id>/version/<int:version_id>/', views.PageReversionAPIView.as_view()),
)
