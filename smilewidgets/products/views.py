from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import datetime
from products.models import ProductPrice, Product

# Create your views here.
@csrf_exempt
# api/get-price will comes here
def get_price(request):
    """This will accept POST request and returns the JSON result 
    """

    # The object which returns the final response
    result = {}

    # We made the API call POST
    if request.method == 'POST':
        try:
            # Convert serialized JSON string to JSON object
            json_input = json.loads(request.body.decode('utf-8'))
            
            # Get the name of the product using the given productCode input
            product_name = str(Product.objects.get(code=json_input.get('productCode'))).split('-')[0].strip()
            
            # Check if the given date falls in blackfriday or not
            if json_input.get('date') in ('2018-11-23', '2018-11-24', '2018-11-25'):
                result['product_name'] = product_name
                # Model based query to get the price if it falls on blackfriday
                result['product_price'] = ProductPrice.objects.get(name=product_name).black_friday_price
            
            #Covert the string representiaon of date to datetime object
            datetime_obj = datetime.strptime(json_input.get('date'), '%Y-%m-%d')

            # Check if the given date >= 2019-01-01
            if datetime_obj >= datetime.strptime('2019-01-01', '%Y-%m-%d'):
                result['product_name'] = product_name                
                # Model based query to get the price if the date falls on next year
                result['product_price'] = ProductPrice.objects.get(name=product_name).next_year_price
        except Exception as e:
            return JsonResponse({'ErrorException raised': str(e)})
        return JsonResponse(result)

    else:
        raise Http404