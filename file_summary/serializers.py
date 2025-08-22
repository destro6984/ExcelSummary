from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from file_summary.fields import ColumnList


class ExcelSummaryInputSerializer(serializers.Serializer):
    file = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["xlsx", "xlsm", "xls"])]
    )
    requested_columns = ColumnList(allow_empty=False)
    sheet = serializers.CharField(required=False)


class ExcelSummaryResultSerializer(serializers.Serializer):
    column = serializers.CharField(allow_blank=True, read_only=True)
    sum = serializers.FloatField(default=0.0, read_only=True)
    avg = serializers.FloatField(default=0.0, read_only=True)


class ExcelSummaryOutputSerializer(serializers.Serializer):
    file = serializers.CharField(max_length=255, default="uploaded.xlsx")
    summary = ExcelSummaryResultSerializer(many=True, required=False)
