from django.db import models
from django.urls import reverse


class Products(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True, unique=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    level1 = models.CharField(max_length=255, blank=True, null=True)
    level2 = models.CharField(max_length=255, blank=True, null=True)
    level3 = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    price_sp = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.CharField(max_length=255, blank=True, null=True)
    properties = models.CharField(max_length=255, blank=True, null=True)
    shared_purchases = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    show_on_main = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    uploaded_csv_id = models.ForeignKey(
        'UploadedCSV', on_delete=models.CASCADE
    )

    class Meta:
        db_table = '_products'

    def get_columns(self):
        return [
            self.code,
            self.name,
            self.level1,
            self.level2,
            self.level3,
            self.price,
            self.price_sp,
            self.quantity,
            self.properties,
            self.shared_purchases,
            self.unit,
            self.image,
            self.show_on_main,
            self.description,
        ]


class UploadedCSV(models.Model):
    DEFAULT_CSV_HEADERS = (
        'Код;Наименование;Уровень1;Уровень2;Уровень3;Цена;'
        'ЦенаСП;Количество;Поля свойств;Совместные покупки;'
        'Единица измерения;Картинка;Выводить на главной;'
        'Описание,,,,,,,,,,,,,,,,,,,,,,'.split(';')
    )

    url = models.URLField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '_uploaded_csv'
        ordering = ['-created_at']

    def get_detailed_url(self):
        return reverse('detail-csv', args=[self.id])

    def get_headers(self):
        h = self.DEFAULT_CSV_HEADERS[:-1]
        h.append(self.DEFAULT_CSV_HEADERS[-1].replace(',', ''))
        return h
