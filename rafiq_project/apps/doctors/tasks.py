from celery import shared_task
from .scraper import scrape_all

@shared_task(name='doctors.tasks.scrape_vezeeta')
def scrape_vezeeta_task(city_slug='egypt'):
    """
    """
    saved, updated = scrape_all(city_slug=city_slug)
    return f'Saved: {saved} | Updated: {updated}'
