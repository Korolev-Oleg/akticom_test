import logging

import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.http import Http404

from csv_parser.models import Products, UploadedCSV

logger = logging.getLogger(__name__)


def get_spreadsheet_id_from_url(url: str) -> str:
    url_separated = url.split('/')

    checks = (
        url_separated[2] == 'docs.google.com',
        url_separated[3] == 'spreadsheets',
        url_separated[4] == 'd',
    )

    if not all(checks):
        raise ValueError('Invalid URL')
    return url_separated[5]


def decode_csv(csv_data) -> str:
    return bytes(csv_data).decode()


def __get_csv_data_from_gsheet(spreadsheet_id: str):
    url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv'
    response = requests.get(url)
    return decode_csv(response.content)


def __create_uploaded_csv(url=None, file_name=None):
    uploaded_csv = UploadedCSV()
    uploaded_csv.url = url
    uploaded_csv.file_name = file_name
    uploaded_csv.save()
    return uploaded_csv


def __make_products_list(
    csv_data: str,
    uploaded_csv_model: UploadedCSV,
) -> list[Products]:
    products_list = []
    count = 0
    for csv_rows in csv_data.splitlines()[1:]:
        csv_cols = csv_rows.split(';')
        product_cols = csv_cols[:13]
        normalized_description = ''.join(csv_cols[13:]).replace(',', '')
        product_cols.append(normalized_description)
        new_product = Products(
            None,
            *product_cols,
        )
        new_product.uploaded_csv_id = uploaded_csv_model
        products_list.append(new_product)
        count += 1

    if not count:
        logger.debug(len(csv_data.splitlines()))
        raise ValueError('No products found')

    logger.info(f'{len(products_list)} products created')
    return products_list


def bulk_update_csv_products(products: list[Products]):
    Products.objects.bulk_create(products)
    logger.debug(f'{len(products)} products pushed in db')


def __handle_csv_data(csv_data: str, url=None, file_name=None):
    with transaction.atomic():
        trans: transaction.Atomic
        uploaded_csv_model = __create_uploaded_csv(url, file_name)
        products_list = __make_products_list(csv_data, uploaded_csv_model)
        bulk_update_csv_products(products_list)

    return uploaded_csv_model.pk


def handle_csv_by_spreadsheet(csv_spreadsheet: str):
    spreadsheet_id = get_spreadsheet_id_from_url(csv_spreadsheet)
    csv_data = __get_csv_data_from_gsheet(spreadsheet_id)
    return __handle_csv_data(csv_data, url=csv_spreadsheet)


def handle_csv_by_file(csv_data, file_name):
    return __handle_csv_data(csv_data, file_name=file_name)


def get_csv_objects():
    return UploadedCSV.objects.all()


def get_detailed_csv(csv_id: int):
    try:
        return Products.objects.select_related('uploaded_csv_id').filter(
            uploaded_csv_id=csv_id
        )
    except Products.DoesNotExist:
        raise Http404(f'file id={csv_id} not found')
