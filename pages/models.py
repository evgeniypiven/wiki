"""
Pages Models
"""

# Standard library imports.

# Related third party imports.
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from ckeditor.fields import RichTextField

# Local application/library specific imports.
from .utils import LocationUploadGenerator


def location_image_upload(instance, filename):
    return LocationUploadGenerator().generate(instance, filename)


class PageManager(models.Manager):
    pass


class Page(models.Model):
    title = models.CharField(
        _('Title'),
        max_length=128,
        null=True,
        blank=True,
        unique=True
    )
    text = RichTextField(
        _('Text'),
        null=True,
        blank=True
    )
    photo = models.ImageField(
        blank=True,
        upload_to=location_image_upload
    )
    dt_created = models.DateTimeField(
        _('Created At'),
        default=timezone.now,
        null=False,
        blank=False,
        help_text=_('Date and time when page was added')
    )
    dt_updated = models.DateTimeField(
        _('Updated At'),
        auto_now=True,
        null=True,
        blank=True,
        help_text=_('Date and time when page was updated')
    )

    objects = PageManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'pages'
        db_table = 'wiki_pages'
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
