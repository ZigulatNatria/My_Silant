from django.urls import path
from .views import MachinaListVew, TOListVew, ComplaintListVew

urlpatterns = [
    path('machine', MachinaListVew.as_view(), name='machine'),
    path('to', TOListVew.as_view(), name='to'),
    path('complaint', ComplaintListVew.as_view(), name='complaint'),
]