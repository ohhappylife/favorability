from datetime import datetime, timedelta
from threading import Timer
import os

x=datetime.today()
y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t=y-x

secs=delta_t.total_seconds()

def autoRun():
    os.system('main.py')
    os.system('vader.py')

t = Timer(secs, autoRun)
t.start()