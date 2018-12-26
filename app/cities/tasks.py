from celery import Celery
from cities import Cities
from selenium.common.exceptions import SessionNotCreatedException

MAX_TRIES = 2

app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')
cities = Cities()

@app.task
def add(x, y):
    return x + y

@app.task
def nyc_zone(address, zip, retry=0):
    try:
        return cities.nyc.get_zone(address, zip)
    except SessionNotCreatedException:
        if retry < MAX_TRIES:
            restart()
            return nyc_zone(address, zip, retry+1)
        else:
            return "NYC lookup failed"

@app.task
def dc_zone(address, zip):
    return cities.dc.get_zone(address, zip)

@app.task
def close():
    cities.close_browser()
    return "Browser closed"

@app.task
def restart():
    global cities
    cities = Cities()
    return "Browser restart"
