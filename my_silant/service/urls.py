from django.urls import path
from .views import MachinaListVew, TOListVew, ComplaintListVew, TOCreateVew, ComplaintCreateVew, MachineCreateVew
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('machine', MachinaListVew.as_view(), name='machine'),
    path('to', login_required(TOListVew.as_view()), name='to'),  #для разнообразия навесил декоратор на URL
    path('complaint', ComplaintListVew.as_view(), name='complaint'),
    path('addto', TOCreateVew.as_view(), name='to_create'),
    path('complaintadd', ComplaintCreateVew.as_view(), name='complaint_create'),
    path('machineadd', MachineCreateVew.as_view(), name='machineadd_create'),
]