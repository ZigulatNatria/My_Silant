from django.urls import path
from .views import TOListVew, ComplaintListVew, TOCreateVew, ComplaintCreateVew,\
    MachineCreateVew, TOUpdateView, ComplaintUpdateView, MachineUpdateView, MachineDeleteView, \
    SearchMachines, hello, by_user_machine, to_detail, complaint_detail, \
    machine_detail, TODeleteView, ComplaintDeleteView, complaint_list_machine, to_list_machine
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('machine', MachinaListVew.as_view(), name='machine'),
    # path('to', login_required(TOListVew.as_view()), name='to'),  #для разнообразия навесил декоратор на URL
    # path('<int:pk>', MachinaDetailVew.as_view(), name='machine_detail'),
    path('hello/', hello, name='hello'), #TODO убрать !!!!
    path('search/', SearchMachines.as_view(), name='search'),
    path('user/', by_user_machine, name='user'),
    path('to/', TOListVew.as_view(), name='to'),
    # path('complaint/', by_user_complaint, name='complaint'),
    path('machineadd', MachineCreateVew.as_view(), name='machine_create'),
    path('addto', TOCreateVew.as_view(), name='to_create'),
    path('complaintadd', ComplaintCreateVew.as_view(), name='complaint_create'),
    path('<int:pk>/medit', MachineUpdateView.as_view(), name='machine_update'),
    path('<int:pk>/tedit', TOUpdateView.as_view(), name='to_update'),
    path('<int:pk>/cedit', ComplaintUpdateView.as_view(), name='complaint_update'),
    path('complaint/', ComplaintListVew.as_view(), name='complaint'),
    path('to/<int:to_id>/', to_detail, name='to_detail'),
    path('complaint/<int:complaint_id>/', complaint_detail, name='complaint_detail'),
    path('machine/<int:machine_id>/', machine_detail, name='machine_detail'),
    path('deletemachine/<int:pk>/', MachineDeleteView.as_view(), name='machine_delete'),
    path('deleteto/<int:pk>/', TODeleteView.as_view(), name='to_delete'),
    path('deleteсo/<int:pk>/', ComplaintDeleteView.as_view(), name='complaint_delete'),
    path('complaintlist/<int:machine_id>/', complaint_list_machine, name='complaint_list'),
    path('tolist/<int:machine_id>/', to_list_machine, name='to_list'),

]