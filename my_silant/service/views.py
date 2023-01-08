from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Machine, TO, Complaint, ServiceCompany
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import TOForm, ComplaintForm, MachineForm
from .filters import MachineFilter, TOFilter, ComplaintFilter

# Create your views here.
# class MachinaListVew(ListView):
#     model = Machine
#     context_object_name = 'machines'
#     template_name = 'machine_list.html'
#     queryset = Machine.objects.all()
#
#
#
# class MachinaDetailVew(DetailView):
#     model = Machine
#     context_object_name = 'machine'
#     template_name = 'machine.html'
#     queryset = Machine.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_aut'] = self.request.user.groups.exists()
#         return context


class TOListVew(LoginRequiredMixin, ListView):
    model = TO
    template_name = 'to.html'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = TOFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class ComplaintListVew(LoginRequiredMixin, ListView):
    model = Complaint
    context_object_name = 'complaint'
    template_name = 'complaint.html'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ComplaintFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


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


# Представления для удаления данных TODO допилить разделение прав
class MachineDeleteView(DeleteView):
    template_name = 'delete_machine.html'
    queryset = Machine.objects.all()
    success_url = '/user/'

class TODeleteView(DeleteView):
    template_name = 'delete_to.html'
    queryset = TO.objects.all()
    success_url = '/to/'

class ComplaintDeleteView(DeleteView):
    template_name = 'delete_complaint.html'
    queryset = Complaint.objects.all()
    success_url = '/complaint/'


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
        else:   # Если данных для поиска нет (search==False)
            machine = 'К сожалению ничего не найдено :('
        context = machine
        return context

    # Функция проверки является ли пользователь авторизованным
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_aut'] = self.request.user.groups.exists()
        return context


# функция фильтрации по авторизованному пользователю
def by_user_machine(request):
    is_aut = request.user.groups.exists()   # Проверка зарегистрировани ли пользователь
    filter = MachineFilter(request.GET) # Фильтрация перебила всю красоту (((((
    if is_aut:   # Если пользователь зарегистрирован
        machine = Machine.objects.filter(client=request.user.first_name) # Фильтруем все строки по полю клиент, если он является пользователем совершающим запрос
        if not machine.exists(): # Если пользователь не является клиентом проверяем является ли он сервисной компанией
            servicelist = ServiceCompany.objects.filter(name=request.user.first_name) # Проверяем есть ли в списке сервисных компаний запись с именм пользователя (сервисная компания)
            if servicelist.exists(): # Если сервисная компания есть в базе идём далее
                service = ServiceCompany.objects.get(name=request.user.first_name) # Т.к. поле сервисной компании в модели Machine является связанным для начала получаем его id
                machine = Machine.objects.filter(service_company=service.id) # По id фильтруем все строки по полю сервисной компании
            else:
                machine = 'К сожалению Ваша техника отсутствует в базе :('
        context = {'machine': machine, 'is_aut': is_aut, 'filter': filter}
    else:
        machine = 'Авторизуйся'
        context = {'machine': machine}
    return render (request, 'user.html', context)


def to_detail(request, to_id):
    is_aut = request.user.groups.exists()
    if is_aut:
        to_d = TO.objects.get(pk=to_id)
        machine = Machine.objects.get(number_machine=to_d.machine_to)
        context = {'to_d': to_d, 'machine': machine, 'is_aut': is_aut}
    else:
        to_d = 'Авторизуйтесь'
        context = {'to_d': to_d}
    return render(request, 'to_detail.html', context)

def complaint_detail(request, complaint_id):
    is_aut = request.user.groups.exists()
    if is_aut:
        complaint_d = Complaint.objects.get(pk=complaint_id)
        machine = Machine.objects.get(number_machine=complaint_d.machine_complaint)
        context = {'complaint_d': complaint_d, 'machine': machine, 'is_aut': is_aut}
    else:
        complaint_d = 'Авторизуйтесь'
        context = {'complaint_d': complaint_d}
    return render(request, 'complaint_detail.html', context)

def complaint_list_machine(request, machine_id): # Вывод всех рекламаций связанных с выбранной машиной
    is_aut = request.user.groups.exists()
    if is_aut:
        complaint_list = Complaint.objects.filter(machine_complaint=machine_id)
        machine = Machine.objects.get(pk=machine_id)
        context = {'complaint_list': complaint_list, 'machine': machine, 'is_aut': is_aut}
    else:
        complaint_list = 'Авторизуйтесь'
        context = {'complaint_list': complaint_list}
    return render(request, 'complaint_list_machine.html', context)


def to_list_machine(request, machine_id): # Вывод всех ТО связанных с выбранной машиной
    is_aut = request.user.groups.exists()
    if is_aut:
        to_list = TO.objects.filter(machine_to=machine_id)
        machine = Machine.objects.get(pk=machine_id)
        context = {'to_list': to_list, 'machine': machine, 'is_aut': is_aut}
    else:
        to_list = 'Авторизуйтесь'
        context = {'to_list': to_list}
    return render(request, 'to_list_machine.html', context)


def machine_detail(request, machine_id):
    is_aut = request.user.groups.exists()
    if is_aut:
        machine = Machine.objects.get(pk=machine_id)
        context = {'machine': machine, 'is_aut': is_aut}
    else:
        machine = 'Авторизуйтесь'
        context = {'machine': machine}
    return render(request, 'machine_detail.html', context)

# Фильтры

def hello(request): #TODO убрать!!!
    return render(request, 'base.html')