from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings




# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
app = Celery('myproject')
app.conf.update(BROKER_URL='redis://default:D3r05IHJjO2CSNi5L7RnPCCD8HhqN8Yh@redis-11512.c16.us-east-1-3.ec2.cloud.redislabs.com:11512',
                CELERY_RESULT_BACKEND='redis://default:D3r05IHJjO2CSNi5L7RnPCCD8HhqN8Yh@redis-11512.c16.us-east-1-3.ec2.cloud.redislabs.com:11512/1')

#result_backend='redis://default:D3r05IHJjO2CSNi5L7RnPCCD8HhqN8Yh@redis-11512.c16.us-east-1-3.ec2.cloud.redislabs.com:11512'
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#app.autodiscover_tasks()
#app.loader.override_backends['django-db'] = 'django_celery_results.backends.database:redis://redistogo:8b576a8323b8164319681bd6b437f856@scat.redistogo.com:10751/'



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

