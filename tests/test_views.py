from pathlib import Path

from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase


TEST_RESPONSES = Path(__file__).parent / "test_files"


class ExcelSummaryViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("excel-get-summary")

    @parameterized.expand(
        [
            (
                ["CURRENT USD"],
                {
                    "column": "CURRENT USD",
                    "summary_length": 1,
                    "avg": 93.5,
                    "sum": 748.0,
                },
            ),
            (
                ["CURRENT CAD", "CURRENT USD"],
                {
                    "column": "CURRENT CAD",
                    "summary_length": 2,
                    "avg": 111.5,
                    "sum": 892.0,
                },
            ),
        ]
    )
    def test_return_correct_response(self, input, expected_data):
        with open(TEST_RESPONSES / "test_correct.xlsx", "rb") as file_obj:
            data = {
                "file": file_obj,
                "requested_columns": input,
            }

            response = self.client.post(self.url, data, format="multipart")

        summary_data = response.json()["summary"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["file"], "test_correct.xlsx")
        self.assertEqual(summary_data[0]["column"], expected_data["column"])
        self.assertEqual(len(summary_data), expected_data["summary_length"])
        self.assertEqual(summary_data[0]["avg"], expected_data["avg"])
        self.assertEqual(summary_data[0]["sum"], expected_data["sum"])

    def test_upload_empty_excel_file(self):
        with open(TEST_RESPONSES / "test_empty.xlsx", "rb") as file_obj:
            data = {
                "file": file_obj,
                "requested_columns": ["price", "qty"],
            }
            response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("file", response.data)
        self.assertIn("The submitted file is empty.", response.data["file"])

    def test_return_missing_fields_response(self):
        response = self.client.post(reverse("excel-get-summary"))
        self.assertEqual(
            response.json(),
            {
                "file": ["No file was submitted."],
                "requested_columns": ["This field is required."],
            },
        )
