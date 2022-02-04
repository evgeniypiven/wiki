"""
Pages admin
"""

# Standard library imports.

# Related third party imports.
from django.contrib import admin
from reversion.admin import VersionAdmin

# Local application/library specific imports.
from .models import Page


class PageAdmin(VersionAdmin):
    list_display = (
        'id', 'dt_created', 'dt_updated',
    )
    readonly_fields = ('dt_created', )

    search_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': (
                'title', 'text', 'photo', 'dt_created'
            )
        }),
    )


admin.site.register(Page, PageAdmin)
