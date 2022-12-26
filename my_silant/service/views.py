from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Machine, TO, Complaint
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import TOForm, ComplaintForm, MachineForm

# Create your views here.


class MachinaListVew(ListView):
    model = Machine
    context_object_name = 'machine'
    template_name = 'machine.html'
    queryset = Machine.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_aut'] = self.request.user.groups.exists()
        return context


class TOListVew(ListView):
    model = TO
    context_object_name = 'to'
    template_name = 'to.html'


class TOCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_to',
        'service.delete_to',
        'service.change_to',
    )
    template_name = 'to_create.html'
    form_class = TOForm


class ComplaintListVew(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Complaint
    context_object_name = 'complaint'
    template_name = 'complaint.html'


class ComplaintCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_complaint',
        'service.delete_complaint',
        'service.change_complaint',
    )
    template_name = 'complaint_create.html'
    form_class = ComplaintForm

class MachineCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_machine',
        'service.delete_machine',
        'service.change_machine',
    )
    template_name = 'machine_create.html'
    form_class = MachineForm