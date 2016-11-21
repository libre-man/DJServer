import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import utils

def index(request):
    return HttpResponse('Hello, World!')

# TODO: bad fix, not secure.
@csrf_exempt
def log_data(request):
    if request.method == 'POST':
        data, time = utils.parse_client_json(request.body)

        response_data = {}
        response_data['success'] = True

        return HttpResponse(json.dumps(response_data),
                content_type='application/json')

    return HttpResponse('')
