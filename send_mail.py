import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apticom.settings")
from django.core.mail import send_mail
for i in range(1,200):
    send_mail('   '+str(i),'','',[''])
print('Done')
