from django.shortcuts import render
from django.views.generic import ListView
from .models import Machine, TO, Complaint

# Create your views here.
class MachinaListVew(ListView):
    model = Machine
    context_object_name = 'machine'
    template_name = 'machine.html'
    queryset = Machine.objects.all()


class TOListVew(ListView):
    model = TO
    context_object_name = 'to'
    template_name = 'to.html'


class ComplaintListVew(ListView):
    model = Complaint
    context_object_name = 'complaint'
    template_name = 'complaint.html'
