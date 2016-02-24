from alexandria import *

r = about()
print(r.url)
print(r.status_code)
print(r.headers['content-type'])
print(r.json())
