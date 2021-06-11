from django.core.management.base import BaseCommand
from scraping.models import Price
from scraping.lazada import checkLazadaPrice


class Command(BaseCommand):
    help = "collect price from shopping platforms"

    # define logic of command
    def handle(self, *args, **options):
        price = checkLazadaPrice("https://www.lazada.sg/products/jabra-elite-active-75t-active-noise-cancellation-true-wireless-sports-earbuds-i659814460-s2001098625.html?spm=a2o42.searchlist.list.9.4dca2277LOJtCb&search=1&freeshipping=1")