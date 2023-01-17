from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Machine, TO, Complaint, ServiceCompany, TechniqueModel, EngineModel, TransmissionModel, \
    DriveAxleModel, SteeringBridgeModel, ServiceType, FailureNode, RecoveryMethod
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import *
from .filters import *
from rest_framework import generics
from .serializers import MachineSerializer, TOSerializer, ComplaintSerializer
# Create your views here.


class TOListVew(LoginRequiredMixin, ListView):
    model = TO
    template_name = 'to.html'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        filter = TOFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        manager = self.request.user.groups.filter(name='Менеджер') # Фильтруем по менеджеру и проверяем
        if not manager.exists():
            is_manager = 'НЕ Менеджер'
        else:
            is_manager = 'Менеджер'
        context = {'filter': filter, 'is_manager': is_manager}
        return context


class ComplaintListVew(LoginRequiredMixin, ListView):
    model = Complaint
    context_object_name = 'complaint'
    template_name = 'complaint.html'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        filter = ComplaintFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        manager = self.request.user.groups.filter(name='Менеджер')
        if not manager.exists():
            is_manager = 'НЕ Менеджер'
        else:
            is_manager = 'Менеджер'
        context = {'filter': filter, 'is_manager': is_manager}
        return context


#Представления для создания TO, Complaint, Machine
class TOCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_to',
    )
    template_name = 'to_create.html'
    form_class = TOForm


class ComplaintCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_complaint',
    )
    template_name = 'complaint_create.html'
    form_class = ComplaintForm

class MachineCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_machine',
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


# Представления для удаления данных
class MachineDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_machine',)
    template_name = 'delete_machine.html'
    queryset = Machine.objects.all()
    success_url = '/user/'

class TODeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_to',)
    template_name = 'delete_to.html'
    queryset = TO.objects.all()
    success_url = '/to/'

class ComplaintDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_complaint',)
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
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'

    filter = MachineFilter(request.GET) # Фильтрация перебила всю красоту (((((
    if is_aut:   # Если пользователь зарегистрирован
        if is_manager == 'Менеджер':
            machine = 0
        else:
            machine = Machine.objects.filter(client=request.user.first_name) # Фильтруем все строки по полю клиент, если он является пользователем совершающим запрос
            if not machine.exists(): # Если пользователь не является клиентом проверяем является ли он сервисной компанией
                servicelist = ServiceCompany.objects.filter(name=request.user.first_name) # Проверяем есть ли в списке сервисных компаний запись с именм пользователя (сервисная компания)
                if servicelist.exists(): # Если сервисная компания есть в базе идём далее
                    service = ServiceCompany.objects.get(name=request.user.first_name) # Т.к. поле сервисной компании в модели Machine является связанным для начала получаем его id
                    machine = Machine.objects.filter(service_company=service.id) # По id фильтруем все строки по полю сервисной компании
                else:
                    machine = 'К сожалению Ваша техника отсутствует в базе :('
        context = {'machine': machine,
                   'is_aut': is_aut,
                   'filter': filter,
                   'is_manager': is_manager
                   }
    else:
        machine = 'Авторизуйся'
        context = {'machine': machine}
    return render (request, 'user.html', context)


def to_detail(request, to_id):
    is_aut = request.user.groups.exists()
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        to_d = TO.objects.get(pk=to_id)
        machine = Machine.objects.get(number_machine=to_d.machine_to)
        service = ServiceType.objects.get(name=to_d.service_type)
        service_company = ServiceCompany.objects.get(name=to_d.company_make_service)
        context = {'to_d': to_d,
                   'machine': machine,
                   'is_aut': is_aut,
                   'service': service,
                   'service_company': service_company,
                   'is_manager': is_manager
                   }
    else:
        to_d = 'Авторизуйтесь'
        context = {'to_d': to_d}
    return render(request, 'to_detail.html', context)

def complaint_detail(request, complaint_id):
    is_aut = request.user.groups.exists()
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        complaint_d = Complaint.objects.get(pk=complaint_id)
        machine = Machine.objects.get(number_machine=complaint_d.machine_complaint)
        node = FailureNode.objects.get(name=complaint_d.failure_node)
        recovery = RecoveryMethod.objects.get(name=complaint_d.recovery_method)
        service = ServiceCompany.objects.get(name=complaint_d.service_company_complaint)
        context = {'complaint_d': complaint_d,
                   'machine': machine,
                   'is_aut': is_aut,
                   'node': node,
                   'recovery': recovery,
                   'service': service,
                   'is_manager': is_manager
                   }
    else:
        complaint_d = 'Авторизуйтесь'
        context = {'complaint_d': complaint_d}
    return render(request, 'complaint_detail.html', context)

def complaint_list_machine(request, machine_id): # Вывод всех рекламаций связанных с выбранной машиной
    is_aut = request.user.groups.exists()
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        complaint_list = Complaint.objects.filter(machine_complaint=machine_id)
        machine = Machine.objects.get(pk=machine_id)
        context = {'complaint_list': complaint_list,
                   'machine': machine,
                   'is_aut': is_aut,
                   'is_manager': is_manager
                   }
    else:
        complaint_list = 'Авторизуйтесь'
        context = {'complaint_list': complaint_list}
    return render(request, 'complaint_list_machine.html', context)


def to_list_machine(request, machine_id): # Вывод всех ТО связанных с выбранной машиной
    is_aut = request.user.groups.exists()
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        to_list = TO.objects.filter(machine_to=machine_id)
        machine = Machine.objects.get(pk=machine_id)
        context = {'to_list': to_list,
                   'machine': machine,
                   'is_aut': is_aut,
                   'is_manager': is_manager
                   }
    else:
        to_list = 'Авторизуйтесь'
        context = {'to_list': to_list}
    return render(request, 'to_list_machine.html', context)


def machine_detail(request, machine_id):
    is_aut = request.user.groups.exists()
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        machine = Machine.objects.get(pk=machine_id)
        technique = TechniqueModel.objects.get(name=machine.technique_model) #Т.к. поле technique_model в модели Machina соответствует полю name модели TechniqueModel
                                                                              #  через него получаем доступ к данным модели TechniqueModel
        engine = EngineModel.objects.get(name=machine.engine_model)
        trans = TransmissionModel.objects.get(name=machine.transmission_model)
        axle = DriveAxleModel.objects.get(name=machine.drive_axle_model)
        steering = SteeringBridgeModel.objects.get(name=machine.steering_bridge_model)
        service = ServiceCompany.objects.get(name=machine.service_company)
        context = {'machine': machine,
                   'technique': technique,
                   'is_aut': is_aut,
                   'engine': engine,
                   'trans': trans,
                   'axle': axle,
                   'steering': steering,
                   'service': service,
                   'is_manager': is_manager
                   }
    else:
        machine = 'Авторизуйтесь'
        context = {'machine': machine}
    return render(request, 'machine_detail.html', context)

# Списки
# Получение списков
class ServiceCompanyListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_servicecompany')
    model = ServiceCompany
    context_object_name = 'servicecompany'
    template_name = 'lists/servicecompany_list.html'
    queryset = ServiceCompany.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ServiceCompanyFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class TechniqueModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_techniquemodel')
    model = TechniqueModel
    context_object_name = 'techniquemodel'
    template_name = 'lists/techniquemodel_list.html'
    queryset = TechniqueModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = TechniqueModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class EngineModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_enginemodel')
    model = EngineModel
    context_object_name = 'enginemodel'
    template_name = 'lists/enginemodel_list.html'
    queryset = EngineModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = EngineModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class TransmissionModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_transmissionmodel')
    model = TransmissionModel
    context_object_name = 'transmissionmodel'
    template_name = 'lists/transmissionmodel_list.html'
    queryset = TransmissionModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = TransmissionModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class DriveAxleModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_driveaxlemodel')
    model = DriveAxleModel
    context_object_name = 'driveaxlemodel'
    template_name = 'lists/driveaxlemodel_list.html'
    queryset = DriveAxleModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = DriveAxleModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class SteeringBridgeModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_steeringbridgemodel')
    model = SteeringBridgeModel
    context_object_name = 'steeringbridgemodel'
    template_name = 'lists/steeringbridgemodel_list.html'
    queryset = SteeringBridgeModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = SteeringBridgeModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class ServiceTypeListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_servicetype')
    model = ServiceType
    context_object_name = 'servicetype'
    template_name = 'lists/servicetype_list.html'
    queryset = ServiceType.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ServiceTypeFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class FailureNodeListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_failurenode')
    model = FailureNode
    context_object_name = 'failurenode'
    template_name = 'lists/failurenode_list.html'
    queryset = FailureNode.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = FailureNodeFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class RecoveryMethodListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_recoverymethod')
    model = RecoveryMethod
    context_object_name = 'recoverymethod'
    template_name = 'lists/recoverymethod_list.html'
    queryset = RecoveryMethod.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = RecoveryMethodFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

# Добавление списков
class ServiceCompanyCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_servicecompany')
    template_name = 'lists/create.html'
    form_class = ServiceCompanyForm
    login_url = '/'


class TechniqueModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_techniquemodel')
    template_name = 'lists/create.html'
    form_class = TechniqueModelForm
    login_url = '/'

class EngineModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_enginemodel')
    template_name = 'lists/create.html'
    form_class = EngineModelForm
    login_url = '/'

class TransmissionModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_transmissionmodel')
    template_name = 'lists/create.html'
    form_class = TransmissionModelForm
    login_url = '/'

class DriveAxleModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_driveaxlemodel')
    template_name = 'lists/create.html'
    form_class = DriveAxleModelForm
    login_url = '/'

class SteeringBridgeModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_steeringbridgemodel')
    template_name = 'lists/create.html'
    form_class = SteeringBridgeModelForm
    login_url = '/'

class ServiceTypeCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_servicetype')
    template_name = 'lists/create.html'
    form_class = ServiceTypeForm
    login_url = '/'

class FailureNodeCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_failurenode')
    template_name = 'lists/create.html'
    form_class = FailureNodeForm
    login_url = '/'

class RecoveryMethodCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_recoverymethod')
    template_name = 'lists/create.html'
    form_class = RecoveryMethodForm
    login_url = '/'

# Формы для удаления списков
class ServiceCompanyDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_servicecompany')
    template_name = 'lists/delete_servicecompany.html'
    queryset = ServiceCompany.objects.all()
    success_url = '/servisecomp/'
    login_url = '/'

class TechniqueModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_techniquemodel')
    template_name = 'lists/delete_techniquemodel.html'
    queryset = TechniqueModel.objects.all()
    success_url = '/modeltech/'
    login_url = '/'

class EngineModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_enginemodel')
    template_name = 'lists/delete_enginemodel.html'
    queryset = EngineModel.objects.all()
    success_url = '/modeleng/'
    login_url = '/'

class TransmissionModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_transmissionmodel')
    template_name = 'lists/delete_transmissionmodel.html'
    queryset = TransmissionModel.objects.all()
    success_url = '/modeltrans/'
    login_url = '/'

class DriveAxleModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_driveaxlemodel')
    template_name = 'lists/delete_driveaxlemodel.html'
    queryset = DriveAxleModel.objects.all()
    success_url = '/modelaxel/'
    login_url = '/'

class SteeringBridgeModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_steeringbridgemodel')
    template_name = 'lists/delete_steeringbridgemodel.html'
    queryset = SteeringBridgeModel.objects.all()
    success_url = '/modelsteer/'
    login_url = '/'

class ServiceTypeDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_servicetype')
    template_name = 'lists/delete_servicetype.html'
    queryset = ServiceType.objects.all()
    success_url = '/servisetype/'
    login_url = '/'

class FailureNodeDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_failurenode')
    template_name = 'lists/delete_failurenode.html'
    queryset = FailureNode.objects.all()
    success_url = '/fnode/'
    login_url = '/'

class RecoveryMethodDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_recoverymethod')
    template_name = 'lists/delete_recoverymethod.html'
    queryset = RecoveryMethod.objects.all()
    success_url = '/reco/'
    login_url = '/'

# Редактирование списков
class ServiceCompanyUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_servicecompany')
    template_name = 'lists/create.html'
    form_class = ServiceCompanyForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return ServiceCompany.objects.get(pk=id)

class TechniqueModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_techniquemodel')
    template_name = 'lists/create.html'
    form_class = TechniqueModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return TechniqueModel.objects.get(pk=id)

class EngineModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_enginemodel')
    template_name = 'lists/create.html'
    form_class = EngineModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return EngineModel.objects.get(pk=id)

class TransmissionModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_transmissionmodel')
    template_name = 'lists/create.html'
    form_class = TransmissionModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return TransmissionModel.objects.get(pk=id)

class DriveAxleModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_driveaxlemodel')
    template_name = 'lists/create.html'
    form_class = DriveAxleModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return DriveAxleModel.objects.get(pk=id)

class SteeringBridgeModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_steeringbridgemodel')
    template_name = 'lists/create.html'
    form_class = SteeringBridgeModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return SteeringBridgeModel.objects.get(pk=id)

class ServiceTypeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_servicetype')
    template_name = 'lists/create.html'
    form_class = ServiceTypeForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return ServiceType.objects.get(pk=id)

class FailureNodeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_failurenode')
    template_name = 'lists/create.html'
    form_class = FailureNodeForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return FailureNode.objects.get(pk=id)

class RecoveryMethodUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_recoverymethod')
    template_name = 'lists/create.html'
    form_class = RecoveryMethodForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return RecoveryMethod.objects.get(pk=id)


# Вьюхи для API
class MachineAPIVew(generics.ListAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class TOAPIVew(generics.ListAPIView):
    queryset = TO.objects.all()
    serializer_class = TOSerializer


class ComplaintAPIVew(generics.ListAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer