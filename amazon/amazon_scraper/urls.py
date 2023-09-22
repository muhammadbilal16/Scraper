from django.urls import path
from .views import ScrapeAmazonDataView

urlpatterns = [
    path('scrape/', ScrapeAmazonDataView.as_view(), name='scrape_amazon_data'),
]
