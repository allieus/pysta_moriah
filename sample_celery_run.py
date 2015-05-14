# -*- coding: utf-8 -*-
from __future__ import unicode_literals

'''
이에 앞서 2가지 작업이 필요하다.

1) celery worker 실행
    shell> celery worker --app pysta --events

2) events monitor 실행
    shell> celery events --app pysta
'''

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pysta.settings")
import django
django.setup()

from timeline.tasks import slow_sum

s = slow_sum.delay(10, 10)
print('task_id : {}'.format(s.task_id))
# http://celery.readthedocs.org/en/latest/reference/celery.result.html#celery.result.AsyncResult.status
print('current status : {}'.format(s.status))
print('waiting for executing ...')

result = s.get()
print('current status : {}'.format(s.status))
print('result : {}'.format(result))

