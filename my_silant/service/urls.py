from django.urls import path
from .views import MachinaListVew, TOListVew, ComplaintListVew, TOCreateVew, ComplaintCreateVew,\
    MachineCreateVew, TOUpdateView, ComplaintUpdateView, MachineUpdateView, MachinaDetailVew, \
    SearchMachines, hello, by_user_machine, by_user_to, to_detail, by_user_complaint, complaint_detail, \
    machine_detail
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('machine', MachinaListVew.as_view(), name='machine'),
    # path('to', login_required(TOListVew.as_view()), name='to'),  #для разнообразия навесил декоратор на URL
    path('complaint', ComplaintListVew.as_view(), name='complaint'),
    path('addto', TOCreateVew.as_view(), name='to_create'),
    path('complaintadd', ComplaintCreateVew.as_view(), name='complaint_create'),
    path('machineadd', MachineCreateVew.as_view(), name='machineadd_create'),
    path('<int:pk>/tedit', TOUpdateView.as_view(), name='to_create'),
    path('<int:pk>/cedit', ComplaintUpdateView.as_view(), name='complaint_create'),
    path('<int:pk>/medit', MachineUpdateView.as_view(), name='machine_create'),
    path('<int:pk>', MachinaDetailVew.as_view(), name='machine_detail'),
    path('hello/', hello, name='hello'), #TODO убрать !!!!
    path('search/', SearchMachines.as_view(), name='search'),
    path('user/', by_user_machine, name='user'),
    path('to/', by_user_to, name='to'),
    path('complaint/', by_user_complaint, name='complaint'),
    path('to/<int:machine_id>/', to_detail, name='to_detail'),
    path('complaint/<int:machine_id>/', complaint_detail, name='complaint_detail'),
    path('machine/<int:machine_id>/', machine_detail, name='machine_detail'),

]