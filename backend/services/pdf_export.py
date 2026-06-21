import io
import logging

logger = logging.getLogger('ats_resume_scorer')

# ---------------------------------------------------------------------------
# PDF backend — try WeasyPrint first (better quality), fall back to xhtml2pdf
# (pure-Python, no native GTK/Cairo required — works on Windows out of the box)
# ---------------------------------------------------------------------------
_pdf_backend: str = 'none'

try:
    from weasyprint import HTML as _WP_HTML
    _pdf_backend = 'weasyprint'
    logger.info('PDF backend: WeasyPrint')
except (ImportError, OSError):
    # WeasyPrint missing or native libs (Cairo/Pango/GObject) not installed
    try:
        from xhtml2pdf import pisa as _pisa  # type: ignore
        _pdf_backend = 'xhtml2pdf'
        logger.info('PDF backend: xhtml2pdf (WeasyPrint native libs unavailable)')
    except ImportError:
        logger.warning('No PDF backend available — PDF export will be disabled.')


def _render_weasyprint(html_docs: dict[str, str]) -> bytes:
    documents = []
    for html_str in html_docs.values():
        doc = _WP_HTML(string=html_str).render()
        documents.append(doc)
    first = documents[0]
    for other in documents[1:]:
        for page in other.pages:
            first.pages.append(page)
    return first.write_pdf()


def _render_xhtml2pdf(html_docs: dict[str, str]) -> bytes:
    # xhtml2pdf renders one HTML string; concatenate all pages into one document
    combined_html = '\n'.join(html_docs.values())
    buf = io.BytesIO()
    result = _pisa.CreatePDF(combined_html, dest=buf)
    if result.err:
        raise RuntimeError(f'xhtml2pdf conversion error: {result.err}')
    return buf.getvalue()


def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    """Convert HTML report sections to a single PDF.

    Uses WeasyPrint if its native libraries are available,
    otherwise falls back to xhtml2pdf (pure-Python, no system libs needed).
    """
    if _pdf_backend == 'weasyprint':
        return _render_weasyprint(html_docs)
    elif _pdf_backend == 'xhtml2pdf':
        return _render_xhtml2pdf(html_docs)
    else:
        raise RuntimeError(
            'PDF generation is unavailable. '
            'Install WeasyPrint (with GTK/Cairo system libraries) '
            'or xhtml2pdf: pip install xhtml2pdf'
        )
