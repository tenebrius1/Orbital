# import json
# from urllib.request import urlopen

# from bs4 import BeautifulSoup
# from django.core.management.base import BaseCommand
# from scraping.models import Job

# class Command(BaseCommand):
#     # define logic of command
#     def handle(self, url):        
#       # collect html
#       html = urlopen(url)  
#       # convert to soup
#       soup = BeautifulSoup(html, 'lxml')        
#       price = soup.find()

#       for p in postings:
#             url = p.find('a', class_='posting-btn-submit')['href']
#             title = p.find('h5').text
#             location = p.find('span', class_='sort-by-location').text
            
#             # check if url in db
#             try:
#                 # save in db
#                 Job.objects.create(
#                     url=url,
#                     title=title,
#                     location=location
#                 )
#                 print('%s added' % (title,))
#             except:
#                 print('%s already exists' % (title,))