# core/cookie.py
def make_set_cookie_header(name, value, path="/"):
    return f"{name}={value}; Path={path}; HttpOnly"


def set_cookie(name, value, headers=None):
    if headers is None:
        headers = {}
    headers["Set-Cookie"] = make_set_cookie_header(name, value)
    return headers


def get_cookie(headers, name):
    cookie_header = headers.get('Cookie', '')
    for cookie in cookie_header.split(';'):
        if '=' in cookie:
            key, value = cookie.strip().split('=', 1)
            if key == name:
                return value
    return None
