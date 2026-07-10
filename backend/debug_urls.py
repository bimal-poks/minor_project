import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver

r = get_resolver()
print("Top-level patterns:")
for p in r.url_patterns:
    print(" -", p)

api_resolver = r.url_patterns[1]
print("\nAPI sub-patterns:")
for p in api_resolver.url_patterns:
    print(" -", p)