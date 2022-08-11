import logging

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.conf import settings
from csv_parser import services
from csv_parser.forms import UploadCSVForm

logger = logging.getLogger(__name__)


def upload_csv(request):
    print(request.FILES)
    return HttpResponse('ok')


def csv_form(request):
    if request.method == 'GET':
        return render(
            request, "csv_parser/index.html", context={'form': UploadCSVForm()}
        )
    if request.method == 'POST':
        uploaded_pk = None
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_spreadsheet = form.cleaned_data['csv_spreadsheet']
            csv_file = form.cleaned_data['csv_file']
            try:
                if csv_spreadsheet:
                    uploaded_pk = services.handle_csv_by_spreadsheet(
                        csv_spreadsheet
                    )
                elif csv_file:
                    uploaded_pk = services.handle_csv_by_file(
                        csv_file, request.FILES.get('csv_file').name
                    )
            except Exception as e:
                if settings.DEBUG:
                    raise e
                logger.error(e)
                return render(
                    request,
                    "csv_parser/index.html",
                    context={'form': form, 'uploading_error': e},
                )

            return render(
                request,
                "csv_parser/index.html",
                context={'form': form, 'uploaded_pk': uploaded_pk},
            )
        return render(request, "csv_parser/index.html", context={'form': form})


def list_csv(requests):
    return render(
        requests,
        "csv_parser/list.html",
        context={'csvs': services.get_csv_objects()},
    )


def detail_csv(request, pk):
    objects = services.get_detailed_csv(pk)
    headers = objects.first().uploaded_csv_id.get_headers()
    return render(
        request,
        'csv_parser/detail.html',
        context={'csv': objects, 'headers': headers},
    )
