from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Machine, TO, Complaint

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


class ComplaintListVew(ListView):
    model = Complaint
    context_object_name = 'complaint'
    template_name = 'complaint.html'


