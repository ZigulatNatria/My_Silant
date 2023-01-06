from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Machine, TO, Complaint
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import TOForm, ComplaintForm, MachineForm

# Create your views here.
class MachinaListVew(ListView):
    model = Machine
    context_object_name = 'machines'
    template_name = 'machine_list.html'
    queryset = Machine.objects.all()



class MachinaDetailVew(DetailView):
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


class ComplaintListVew(LoginRequiredMixin, ListView):
    model = Complaint
    context_object_name = 'complaint'
    template_name = 'complaint.html'


#Представления для создания TO, Complaint, Machine
class TOCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_to',
        'service.delete_to',
    )
    template_name = 'to_create.html'
    form_class = TOForm


class ComplaintCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_complaint',
        'service.delete_complaint',
    )
    template_name = 'complaint_create.html'
    form_class = ComplaintForm

class MachineCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_machine',
        'service.delete_machine',
    )
    template_name = 'machine_create.html'
    form_class = MachineForm

#Представления для редактирования TO, Complaint, Machine
class TOUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_to',)
    template_name = 'to_create.html'
    form_class = TOForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return TO.objects.get(pk=id)


class ComplaintUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_complaint',)
    template_name = 'complaint_create.html'
    form_class = ComplaintForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Complaint.objects.get(pk=id)

class MachineUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_machine',)
    template_name = 'machine_create.html'
    form_class = MachineForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Machine.objects.get(pk=id)

class SearchMachines(ListView):
    model = Machine
    template_name = 'search.html'
    context_object_name = 'machine'

    # Функция поиска
    def get_queryset(self, **kwargs):
        search_query = self.request.GET.get('search', '') # Получаем данные из запроса (search)
        if search_query:   # Если данные есть (search==True)
            machine = Machine.objects.filter(number_machine__icontains=search_query) # Фильтруем по данным из search
            if not machine.exists():  # Если в таблице базы таких данных нет, то присваиваем строке значение о том что их нет )))
                machine = 'К сожалению ничего не найдено :('
        else:   # Если данных для поиска нет (search==Fulse)
            machine = 'К сожалению ничего не найдено :('
        context = machine
        return context

    # Функция проверки является ил пользователь авторизованным
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_aut'] = self.request.user.groups.exists()
        return context




def hello(request): #TODO убрать!!!
    return render(request, 'base.html')