import re
prefix='/dex_1'
pattern = r"(href|action)=([\'\"])\/(?!" + re.escape(prefix.lstrip('/')) + r")"
s = '... <link rel="stylesheet" href="/static/css/register.css"> <form action="/login"> <a href="/dex_1/ok">'
print('PATTERN:',pattern)
res = re.sub(pattern, r"\1=\2"+prefix+r"/", s)
print('BEFORE:', s)
print('AFTER: ', res)
