from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

import pandas as pd
from rest_framework.viewsets import ViewSet

from file_summary.serializers import (
    ExcelSummaryInputSerializer,
    ExcelSummaryOutputSerializer,
)
from file_summary.utlis import find_cell


class ExcelSummaryView(ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        request=ExcelSummaryInputSerializer,
        responses=ExcelSummaryOutputSerializer,
        tags=["Excel"],
    )
    @action(detail=False, methods=["post"])
    def get_summary(self, request, *args, **kwargs):
        serializer = ExcelSummaryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        excel_file = serializer.validated_data["file"]
        requested_columns = serializer.validated_data["requested_columns"]
        sheet = serializer.validated_data.get("sheet")

        df = pd.read_excel(excel_file, header=None, sheet_name=sheet or 0)

        if df.empty:
            return Response(
                {"detail": "The sheet is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = []
        for col_name in requested_columns:
            found_loc = find_cell(df, col_name)
            if not found_loc:
                continue

            header_row_idx, col_idx = found_loc

            # Everything **below** the header cell in the same column
            col_series = df.iloc[header_row_idx + 1 :, col_idx]

            # Convert to numeric; non-numeric -> NaN -> ignored
            nums = pd.to_numeric(col_series, errors="coerce")
            count = int(nums.notna().sum())
            col_sum = float(nums.sum(skipna=True)) if count else 0.0
            col_avg = float(nums.mean(skipna=True)) if count else 0.0

            summary.append(
                {
                    "column": col_name,
                    "sum": col_sum,
                    "avg": col_avg,
                }
            )
        serializer_response = ExcelSummaryOutputSerializer(
            {"file": getattr(excel_file, "name"), "summary": summary}
        )
        return Response(serializer_response.data, status=status.HTTP_200_OK)
