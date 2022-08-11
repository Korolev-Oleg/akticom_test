import logging

from django import forms

from csv_parser import services
from csv_parser.models import UploadedCSV


logger = logging.getLogger(__name__)


class UploadCSVForm(forms.Form):
    csv_spreadsheet = forms.URLField(
        label='Google spreadsheet url', required=False
    )
    csv_file: str = forms.FileField(required=False)

    def clean_csv_spreadsheet(self):
        csv_spreadsheet = self.cleaned_data['csv_spreadsheet']
        if csv_spreadsheet:
            try:
                services.get_spreadsheet_id_from_url(csv_spreadsheet)
            except Exception as e:
                logger.error(e)
                raise forms.ValidationError('Не верный spreadsheet url')
        return csv_spreadsheet

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if csv_file is None:
            return None

        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('Файл не CSV')

        csv_data = services.decode_csv(csv_file.read())
        headers = csv_data.splitlines()[0].split(';')
        if headers != UploadedCSV.DEFAULT_CSV_HEADERS:
            raise forms.ValidationError('Не верный формат CSV')

        if len(csv_data.splitlines()) < 2:
            raise forms.ValidationError('Файл пустой')

        return csv_data

    def clean(self):
        cleaned_data = super().clean()
        csv_spreadsheet = cleaned_data.get('csv_spreadsheet')
        csv_file = cleaned_data.get('csv_file')
        if not csv_spreadsheet and not csv_file:
            raise forms.ValidationError('Не выбран файл или spreadsheet')
        return cleaned_data
