from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tinydb import TinyDB
from tinydb import where
from functools import reduce
import operator
import re
import datetime


def check_types(value):
    if re.match(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$|'
                  r'^(19|20)\d\d\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$', value):
        return 'date'
    elif re.match(r'^(\+7|8)\d{10}$', value):
        return 'phone'
    elif re.match(r"^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z0]+$", value):
        return 'email'
    else:
        return 'text'


def add_types_to_dict(fields_values):
    for i in fields_values:
        fields_values[i] = [
            fields_values[i],
            check_types(fields_values[i])
        ]
        if fields_values[i][1] == 'date':
            try:
                date = datetime.datetime.strptime(fields_values[i][0], '%d.%m.%Y')
            except ValueError:
                date = datetime.datetime.strptime(fields_values[i][0], '%Y-%m-%d')
            fields_values[i][0] = date.strftime('%d.%m') + '.' + date.strftime('%Y')
    return fields_values


@csrf_exempt
def get_form(request):
    db = TinyDB('test_db.json')
    if request.method == 'POST':
        fields_values = request.POST.dict()
        conditions = []
        add_types_to_dict(fields_values)
        for field_name, value_type in fields_values.items():
            value, type_ = value_type
            if db.contains(where('fields').any((where(field_name) == value) & (where('type') == type_))):
                conditions.append(where('fields').any((where(field_name) == value) & (where('type') == type_)))
        if conditions:
            query = reduce(operator.and_, conditions)
            form_templates = db.search(query)
            return HttpResponse(f"{', '.join([form['name_template'] for form in form_templates])}")
        else:
            error_dict = {key: value[1] for key, value in fields_values.items()}
            return JsonResponse(error_dict)
