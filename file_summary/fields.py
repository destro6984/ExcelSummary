from rest_framework import serializers


class ColumnList(serializers.ListField):
    """
    Custom ListField for multipart form inputs.
        Accepts:
          - a single CSV string wrapped in a list, e.g.:
              ['price, qty']
            → ["price", "qty"]
        Always returns a list[str].
    """

    child = serializers.CharField(allow_blank=False)

    def to_internal_value(self, data):
        if isinstance(data, list) and len(data) == 1 and isinstance(data[0], str):
            val = data[0].strip()
            # treat as comma-separated string
            if "," in val:
                items = [s.strip() for s in val.split(",") if s.strip()]
                return super().to_internal_value(items)
            # Single item string
            return super().to_internal_value([val])

        return super().to_internal_value(data)
