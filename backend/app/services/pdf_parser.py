from dataclasses import dataclass

import fitz


class PdfParseError(Exception):
    """Raised when a PDF cannot be opened or read."""


@dataclass(frozen=True)
class PdfTextExtraction:
    raw_text: str
    page_count: int


def extract_text_from_pdf(file_content: bytes) -> PdfTextExtraction:
    if not file_content:
        raise ValueError("PDF file is empty")

    try:
        with fitz.open(stream=file_content, filetype="pdf") as document:
            if document.needs_pass:
                raise PdfParseError("Password-protected PDF is not supported")

            page_texts = []
            for page in document:
                page_texts.append(page.get_text("text"))

            return PdfTextExtraction(
                raw_text="\n\n".join(page_texts),
                page_count=document.page_count,
            )
    except PdfParseError:
        raise
    except Exception as exc:
        raise PdfParseError("Unable to parse PDF file") from exc

