import mimetypes
import settings


def render_template(filename, context=None, use_base=True):
    if context is None:
        context = {}

    child_path = settings.TEMPLATE_DIR / filename
    if not child_path.exists():
        return None
    child_html = child_path.read_text(encoding="utf-8")

    # جایگزینی متغیرها در قالب فرزند
    for key, value in context.items():
        child_html = child_html.replace(f"{{{{ {key} }}}}", str(value))

    # فقط اگر use_base=True باشد و فایل base.html وجود داشته باشد، آن را اعمال کن
    if use_base:
        base_path = settings.TEMPLATE_DIR / "base.html"
        if base_path.exists():
            base_html = base_path.read_text(encoding="utf-8")
            base_html = base_html.replace(
                "{{ navigation }}", context.get("navigation", ""))
            base_html = base_html.replace(
                "{{ title }}", context.get("title", "Ez Dex"))
            base_html = base_html.replace(
                "{{ extra_head }}", context.get("extra_head", ""))
            base_html = base_html.replace("{{ content }}", child_html)
            return base_html

    return child_html


def serve_static_file(path):
    if not path.startswith(settings.STATIC_URL_PREFIX):
        return None
    relative_path = path[len(settings.STATIC_URL_PREFIX):]
    file_path = settings.STATIC_DIR / relative_path
    if not file_path.exists() or not file_path.is_file():
        return None
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = "application/octet-stream"
    try:
        with open(file_path, 'rb') as f:
            body = f.read()
        return (body, 200, {"Content-Type": content_type})
    except IOError:
        return None


def redirect(location, headers=None):
    if headers is None:
        headers = {}
    headers["Location"] = location
    return ("", 302, headers)


def _200(html, headers=None):
    response_headers = {"Content-Type": "text/html; charset=utf-8"}
    if headers:
        response_headers.update(headers)
    return (html, 200, response_headers)


def _401(message="Unauthorized"):
    return (message, 401, {"Content-Type": "text/plain; charset=utf-8"})


def _403(message="Forbidden"):
    return (message, 403, {"Content-Type": "text/plain; charset=utf-8"})


def _404():
    return ("Page Not Found", 404, {"Content-Type": "text/plain; charset=utf-8"})


def _500():
    return ("Internal Server Error", 500, {"Content-Type": "text/plain; charset=utf-8"})
