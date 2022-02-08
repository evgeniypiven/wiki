"""
Pages API Views
"""

# Standard library imports.

# Related third party imports.
import reversion
from reversion.models import Version
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.db import transaction

# Local application/library specific imports.
from pages.models import Page
from pages.serializers import PagesSerializer, VersionSerializer


class PagesListAPIView(generics.ListAPIView):
    """
    Endpoint to get a list of all pages
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PagesSerializer
    queryset = Page.objects.all()


class PageVersionsListAPIView(generics.ListAPIView):
    """
    Endpoint to get a list of all page versions
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = VersionSerializer

    def get(self, request, *args, **kwargs):
        """
        Checks if page exists.
        Returns a JSON page versions list.
        """
        try:
            page = Page.objects.get(id=self.kwargs['page_id'])
        except Page.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        result = Version.objects.get_for_object(page)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PageDetailAPIView(generics.RetrieveAPIView):
    """
    Endpoint to get details of specific page
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PagesSerializer

    def get_object(self):
        return get_object_or_404(Page, pk=self.kwargs['page_id'])


class PageDetailVersionAPIView(generics.RetrieveAPIView):
    """
    Endpoint to get details of specific page version
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PagesSerializer

    def get(self, request, *args, **kwargs):
        """
        Checks if page exists.
        Checks if page version exists.
        Returns a JSON page version.
        """
        try:
            page = Page.objects.get(id=self.kwargs['page_id'])
        except Page.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        result = get_object_or_404(Version.objects.get_for_object(page),
                                   pk=self.kwargs['version_id'])

        serializer = self.get_serializer(result.field_dict)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PageUpdateAPIView(generics.UpdateAPIView):
    """
    Endpoint to update specific page
    """
    queryset = Page.objects.all()
    serializer_class = PagesSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(Page, id=self.kwargs['page_id'])

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Checks is page exists.
        Returns a JSON of updated page details.
        """
        page = self.get_object()
        serializer = self.get_serializer(page, data=request.data)

        if serializer.is_valid():
            with transaction.atomic(), reversion.create_revision():
                serializer.save()
                reversion.set_user(request.user)
                reversion.set_comment("Updated.")

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageReversionAPIView(generics.UpdateAPIView):
    """
    Endpoint to revert page to specific version.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PagesSerializer

    def get_object(self):
        return get_object_or_404(Page, pk=self.kwargs['page_id'])

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Checks if page and version exists.
        Returns a JSON of reverted page details.
        """
        page = self.get_object()
        serializer = self.get_serializer(page, data=request.data)

        if serializer.is_valid():
            revision = get_object_or_404(Version.objects.get_for_object(page),
                                         pk=self.kwargs['version_id']).revision
            with transaction.atomic(), reversion.create_revision():
                reversion.set_user(request.user)
                reversion.set_comment("Page reversion to version #{}".format(revision.id))
                revision.revert()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
