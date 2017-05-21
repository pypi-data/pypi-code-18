from django.conf import settings


ARCGIS_UPLOAD_ITEM_TO = getattr(
    settings,
    'ARCGIS_UPLOAD_ITEM_TO',
    'arcgis/items/%Y/%m/'
)
