import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import attendance.urls as att_urls

print("attendance.urls file location:", att_urls.__file__)
print("\nattendance.urls patterns:")
for p in att_urls.urlpatterns:
    print(" -", p)