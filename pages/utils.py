"""
Pages Utils
"""

# Standard library imports.

# Related third party imports.
from django.utils import timezone

# Local application/library specific imports.
from wiki.utils.files.utils import UploadToGeneratorBase


class LocationUploadGenerator(UploadToGeneratorBase):
    def construct_path(self, instance, filename) -> str:
        return f'pages/title_photo/'

    def construct_filename(self, instance, filename) -> str:
        dt_part = timezone.now().strftime('%Y%m%d_%H%M%S')
        ext = self.get_extension(filename, True, True)
        name = f'pages_{instance.pk}_{dt_part}'
        return f'{name}{ext}'


location_upload_to = LocationUploadGenerator().generate
