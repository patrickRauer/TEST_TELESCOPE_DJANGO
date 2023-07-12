from celery import shared_task
from bs4 import BeautifulSoup
import requests

from .models import Page, Data


@shared_task
def collect_weather_data():
    """
    Collect weather data for later usage
    """
    page = Page.objects.last()
    response = requests.get(page.url)
    bs = BeautifulSoup(response.text, parser='html')
    tables = bs.findAll('table')
