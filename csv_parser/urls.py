from django.urls import path

from csv_parser import views

urlpatterns = [
    path('', views.csv_form, name='csv-form'),
    path('list-csvs', views.list_csv, name='list-csv'),
    path('detail-csv/<int:pk>', views.detail_csv, name='detail-csv'),
]
