from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Machine, TO, Complaint, ServiceCompany
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
    if is_aut:   # Если пользователь зарегистрирован
        machine = Machine.objects.filter(client=request.user.first_name) # Фильтруем все строки по полю клиент, если он является пользователем совершающим запрос
        if not machine.exists(): # Если пользователь не является клиентом проверяем является ли он сервисной компанией
            servicelist = ServiceCompany.objects.filter(name=request.user.first_name) # Проверяем есть ли в списке сервисных компаний запись с именм пользователя (сервисная компания)
            if servicelist.exists(): # Если сервисная компания есть в базе идём далее
                service = ServiceCompany.objects.get(name=request.user.first_name) # Т.к. поле сервисной компании в модели Machine является связанным для начала получаем его id
                machine = Machine.objects.filter(service_company=service.id) # По id фильтруем все строки по полю сервисной компании
            else:
                machine = 'К сожалению Ваша техника отсутствует в базе :('
        context = {'machine': machine, 'is_aut': is_aut}
    else:
        machine = 'Авторизуйся'
        context = {'machine': machine}
    return render (request, 'user.html', context)


def by_user_to(request):
    is_aut = request.user.groups.exists()   # Проверка зарегистрировани ли пользователь
    if is_aut:   # Если пользователь зарегистрирован
        machine = Machine.objects.filter(client=request.user.first_name) # Фильтруем все строки по полю клиент, если он является пользователем совершающим запрос
        if not machine.exists(): # Если пользователь не является клиентом проверяем является ли он сервисной компанией
            servicelist = ServiceCompany.objects.filter(name=request.user.first_name) # Проверяем есть ли в списке сервисных компаний запись с именм пользователя (сервисная компания)
            if servicelist.exists(): # Если сервисная компания есть в базе идём далее
                service = ServiceCompany.objects.get(name=request.user.first_name) # Т.к. поле сервисной компании в модели Machine является связанным для начала получаем его id
                machine = Machine.objects.filter(service_company=service.id) # По id фильтруем все строки по полю сервисной компании
            else:
                to = 'Нет данных по ТО'
        if machine.exists(): # Если machine==True (тобишь у пользователя есть ТО в базе)
            for m in machine:
                m.number_machine = machine.filter(id__in=m.number_machine) # Получаем все номера машин связанных с пользователем
                # to = TO.objects.filter(machine_to=m)
                to = m.number_machine

            context = {'to': to, 'is_aut': is_aut}
        context = {'to': to, 'is_aut': is_aut}
    else:
        to = 'Авторизуйся'
        context = {'to': to}
    return render (request, 'to.html', context)


def by_user_complaint(request):
    is_aut = request.user.groups.exists()   # Проверка зарегистрировани ли пользователь
    if is_aut:   # Если пользователь зарегистрирован
        machine = Machine.objects.filter(client=request.user.first_name) # Фильтруем все строки по полю клиент, если он является пользователем совершающим запрос
        if not machine.exists(): # Если пользователь не является клиентом проверяем является ли он сервисной компанией
            servicelist = ServiceCompany.objects.filter(name=request.user.first_name) # Проверяем есть ли в списке сервисных компаний запись с именм пользователя (сервисная компания)
            if servicelist.exists(): # Если сервисная компания есть в базе идём далее
                service = ServiceCompany.objects.get(name=request.user.first_name) # Т.к. поле сервисной компании в модели Machine является связанным для начала получаем его id
                machine = Machine.objects.filter(service_company=service.id) # По id фильтруем все строки по полю сервисной компании
            else:
                complaint = 'Нет данных о рекламациях'
        if machine.exists(): # Если machine==True (тобишь у пользователя есть ТО в базе)
            for m in machine:
                m.number_machine = machine.filter(id__in=m.number_machine) # Получаем все номера машин связанных с пользователем
                # to = TO.objects.filter(machine_to=m)
                complaint = m.number_machine

            context = {'complaint': complaint, 'is_aut': is_aut}
        context = {'complaint': complaint, 'is_aut': is_aut}
    else:
        complaint = 'Авторизуйтесь'
        context = {'complaint': complaint}
    return render (request, 'complaint.html', context)


def to_detail(request, machine_id):
    is_aut = request.user.groups.exists()
    if is_aut:
        to_d = TO.objects.filter(machine_to=machine_id)
        machine = Machine.objects.get(pk=machine_id)
        context = {'to_d': to_d, 'machine': machine, 'is_aut': is_aut}
    else:
        to_d = 'Авторизуйтесь'
        context = {'to_d': to_d}
    return render(request, 'to_detail.html', context)

def complaint_detail(request, machine_id):
    is_aut = request.user.groups.exists()
    if is_aut:
        complaint_d = Complaint.objects.filter(machine_complaint=machine_id)
        machine = Machine.objects.get(pk=machine_id)
        context = {'complaint_d': complaint_d, 'machine': machine, 'is_aut': is_aut}
    else:
        complaint_d = 'Авторизуйтесь'
        context = {'complaint_d': complaint_d}
    return render(request, 'complaint_detail.html', context)

def machine_detail(request, machine_id):
    is_aut = request.user.groups.exists()
    if is_aut:
        machine = Machine.objects.get(pk=machine_id)
        context = {'machine': machine, 'is_aut': is_aut}
    else:
        machine = 'Авторизуйтесь'
        context = {'machine': machine}
    return render(request, 'machine_detail.html', context)


def hello(request): #TODO убрать!!!
    return render(request, 'base.html')