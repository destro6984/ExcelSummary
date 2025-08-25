from django.urls import path
from rest_framework.routers import DefaultRouter

from file_summary.views import ExcelSummaryView

urlpatterns = [
    path("excel/summary/", ExcelSummaryView.as_view({"post": "get_summary"}), name="excel-summary"),
]
