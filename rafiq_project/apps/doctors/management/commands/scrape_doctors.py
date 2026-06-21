from django.core.management.base import BaseCommand
from apps.doctors.scraper import CITY_SLUGS, scrape_city, scrape_all
import time


class Command(BaseCommand):
    help = "Scrape doctors from Vezeeta"

    def add_arguments(self, parser):
        parser.add_argument(
            "--city",
            choices=list(CITY_SLUGS.keys()),
            help="Scrape one city only. Without it → all cities.",
        )

    def handle(self, *args, **options):

        city = options.get("city")

        if city:
            self.stdout.write(f" Scraping city: {city}")
            scrape_city(
                city,
                CITY_SLUGS[city],
                log=self.stdout.write,
            )

        else:
            self.stdout.write("Scraping ALL cities")
            scrape_all(
                city_slug="egypt",
                log=self.stdout.write,
            )

        self.stdout.write(
            self.style.SUCCESS("Scraping Complete!")
        )
