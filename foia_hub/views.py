from django.http import HttpResponse
import datetime

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('foia_hub', 'templates'))

import json
from django.core.serializers.json import DjangoJSONEncoder

from foia_hub.models import *

def request_form(request, slug=None):
    template = env.get_template('request/form.html')
    return HttpResponse(template.render(slug=slug))

def request_start(request):

    template = env.get_template('request/index.html')
    return HttpResponse(template.render())


# similar to agency API, but optimized for typeahead consumption
def request_autocomplete(request):
    agencies = Agency.objects.order_by('name').all()
    response = []
    for agency in agencies:
        response.append({
            "name": agency.name,
            "description": agency.description,
            "abbreviation": agency.abbreviation,
            "slug": agency.slug
        })
    agency_json = json.dumps(response, cls=DjangoJSONEncoder)
    return HttpResponse(agency_json, content_type = "application/json")