import mimetypes
import settings


def render_template(filename, context=None):
    template_path = settings.TEMPLATE_DIR / filename
    if not template_path.exists():
        return None
    html = template_path.read_text(encoding="utf-8")
    if context:
        for key, value in context.items():
            html = html.replace(f"{{{{ {key} }}}}", str(value))
    return html


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
