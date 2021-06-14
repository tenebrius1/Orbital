from datetime import datetime

from django.core.management.base import BaseCommand
from scraping.amazon import checkAmazonPrice
from scraping.lazada import checkLazadaPrice
from scraping.models import Price
from scraping.shopee import checkShopeePrice


class Command(BaseCommand):
    help = "collect price from shopping platforms"

    # define logic of command
    def handle(self, *args, **options):
        # Update DB
        entries = Price.objects.all()
        curr_date = datetime.now().strftime("%m/%d/%Y")

        # Loops through each entry in the database and updates them
        for entry in entries:
            if "lazada" in entry.url:
               price = float("{:.2f}".format(float(checkLazadaPrice(entry.url)[1:])))
            elif "shopee" in entry.url:
               price = float("{:.2f}".format(float(checkShopeePrice(entry.url)[1:])))
            elif "amazon" in entry.url:
               price = float("{:.2f}".format(float(checkAmazonPrice(entry.url)[2:])))
            else:
               pass
            
            entry.priceArr.append(price)
            entry.dateArr.append(curr_date)
            entry.save()
        
        self.stdout.write('job complete')
