import os
import subprocess
import tempfile
from unittest import TestCase


class TestChromiumPDFGeneration(TestCase):
    def setUp(self):
        self.chrome_path = os.environ.get("CHROME_BIN_PATH", "/usr/bin/chromium")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html") as f:
            self.html_path = f.name
            f.write(
                "<html><body><h1>Test Invoice</h1><p>Test Content</p></body></html>"
            )
            f.flush()

        self.pdf_output_path = self.html_path.replace(".html", ".pdf")

    def tearDown(self):
        if os.path.exists(self.pdf_output_path):
            os.remove(self.pdf_output_path)

    def test_pdf_output_is_valid(self):
        self.assertTrue(os.path.exists(self.chrome_path))

        result = subprocess.run(
            [
                self.chrome_path,
                "--headless",
                "--no-sandbox",
                "--disable-gpu",
                f"--print-to-pdf={self.pdf_output_path}",
                "--no-pdf-header-footer",
                f"file://{self.html_path}",
            ],
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(self.pdf_output_path))

        # Check if valid pdf file signature
        with open(self.pdf_output_path, "rb") as f:
            header = f.read(4)
        self.assertEqual(header, b"%PDF")
