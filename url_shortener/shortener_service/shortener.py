"""URL shortener business object classes"""


class UrlShortener:  # pylint: disable=too-few-public-methods
    """URL shortener business object class"""

    def __init__(self, id, long_url, short_url, created):  # pylint: disable=redefined-builtin
        self.id = id
        self.long_url = long_url
        self.short_url = short_url
        self.created = created

    def dict(self):
        """Render as dictionaries"""
        return {
            "id": self.id,
            "long_url": self.long_url,
            "short_url": self.short_url,
            "created": self.created,
        }
