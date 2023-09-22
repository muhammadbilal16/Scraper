from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .scraping_logic import scrape_amazon_data
from .serializers import ProductSerializer

class ScrapeAmazonDataView(APIView):
    def post(self, request):
        try:
        
            url = request.data.get('url')
            print(f"Received URL: {url}")

            if not url:
                return Response({'error': 'URL not provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            product = scrape_amazon_data(url)

            if not product:
                return Response({'error': 'Failed to scrape data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

            serializer = ProductSerializer(product)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
