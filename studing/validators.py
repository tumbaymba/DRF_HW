from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url_valid = value.get(self.field)
        if url_valid:
            if 'www.youtube.com/' in url_valid:
                return value
            raise ValidationError('Ссылки на сторонние видео запрещены')