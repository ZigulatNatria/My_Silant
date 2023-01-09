from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Machine, TO, Complaint, ServiceCompany, TechniqueModel, EngineModel, TransmissionModel, \
    DriveAxleModel, SteeringBridgeModel, ServiceType, FailureNode, RecoveryMethod
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import *
from .filters import *
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

# Списки
# Получение списков
class ServiceCompanyListView(ListView):
    model = ServiceCompany
    context_object_name = 'servicecompany'
    template_name = 'lists/servicecompany_list.html'
    queryset = ServiceCompany.objects.all()

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ServiceCompanyFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class TechniqueModelListView(ListView):
    model = TechniqueModel
    context_object_name = 'techniquemodel'
    template_name = 'lists/techniquemodel_list.html'
    queryset = TechniqueModel.objects.all()

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = TechniqueModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class EngineModelListView(ListView):
    model = EngineModel
    context_object_name = 'enginemodel'
    template_name = 'lists/enginemodel_list.html'
    queryset = EngineModel.objects.all()

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = EngineModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class TransmissionModelListView(ListView):
    model = TransmissionModel
    context_object_name = 'transmissionmodel'
    template_name = 'lists/transmissionmodel_list.html'
    queryset = TransmissionModel.objects.all()

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = TransmissionModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class DriveAxleModelListView(ListView):
    model = DriveAxleModel
    context_object_name = 'driveaxlemodel'
    template_name = 'lists/driveaxlemodel_list.html'
    queryset = DriveAxleModel.objects.all()

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = DriveAxleModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class SteeringBridgeModelListView(ListView):
    model = SteeringBridgeModel
    context_object_name = 'steeringbridgemodel'
    template_name = 'lists/steeringbridgemodel_list.html'
    queryset = SteeringBridgeModel.objects.all()

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = SteeringBridgeModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class ServiceTypeListView(ListView):
    model = ServiceType
    context_object_name = 'servicetype'
    template_name = 'lists/servicetype_list.html'
    queryset = ServiceType.objects.all()

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ServiceTypeFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class FailureNodeListView(ListView):
    model = FailureNode
    context_object_name = 'failurenode'
    template_name = 'lists/failurenode_list.html'
    queryset = FailureNode.objects.all()

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = FailureNodeFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class RecoveryMethodListView(ListView):
    model = RecoveryMethod
    context_object_name = 'recoverymethod'
    template_name = 'lists/recoverymethod_list.html'
    queryset = RecoveryMethod.objects.all()

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = RecoveryMethodFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

# Добавление списков
class ServiceCompanyCreateVew(CreateView):
    template_name = 'lists/create.html'
    form_class = ServiceCompanyForm


class TechniqueModelCreateVew(CreateView):
    template_name = 'lists/create.html'
    form_class = TechniqueModelForm

class EngineModelCreateVew(CreateView):
    template_name = 'lists/create.html'
    form_class = EngineModelForm

class TransmissionModelCreateVew(CreateView):
    template_name = 'lists/create.html'
    form_class = TransmissionModelForm

class DriveAxleModelCreateVew(CreateView):
    template_name = 'lists/create.html'
    form_class = DriveAxleModelForm

class SteeringBridgeModelCreateVew(CreateView):
    template_name = 'lists/create.html'
    form_class = SteeringBridgeModelForm

class ServiceTypeCreateVew(CreateView):
    template_name = 'lists/create.html'
    form_class = ServiceTypeForm

class FailureNodeCreateVew(CreateView):
    template_name = 'lists/create.html'
    form_class = FailureNodeForm

class RecoveryMethodCreateVew(CreateView):
    template_name = 'lists/create.html'
    form_class = RecoveryMethodForm

# Формы для удаления списков
class ServiceCompanyDeleteView(DeleteView):
    # permission_required = ('',)
    template_name = 'lists/delete_servicecompany.html'
    queryset = ServiceCompany.objects.all()
    success_url = '/servisecomp/'

class TechniqueModelDeleteView(DeleteView):
    # permission_required = ('',)
    template_name = 'lists/delete_techniquemodel.html'
    queryset = TechniqueModel.objects.all()
    success_url = '/modeltech/'

class EngineModelDeleteView(DeleteView):
    # permission_required = ('',)
    template_name = 'lists/delete_enginemodel.html'
    queryset = EngineModel.objects.all()
    success_url = '/modeleng/'

class TransmissionModelDeleteView(DeleteView):
    # permission_required = ('',)
    template_name = 'lists/delete_transmissionmodel.html'
    queryset = TransmissionModel.objects.all()
    success_url = '/modeltrans/'

class DriveAxleModelDeleteView(DeleteView):
    # permission_required = ('',)
    template_name = 'lists/delete_driveaxlemodel.html'
    queryset = DriveAxleModel.objects.all()
    success_url = '/modelaxel/'

class SteeringBridgeModelDeleteView(DeleteView):
    # permission_required = ('',)
    template_name = 'lists/delete_steeringbridgemodel.html'
    queryset = SteeringBridgeModel.objects.all()
    success_url = '/modelsteer/'

class ServiceTypeDeleteView(DeleteView):
    # permission_required = ('',)
    template_name = 'lists/delete_servicetype.html'
    queryset = ServiceType.objects.all()
    success_url = '/servisetype/'

class FailureNodeDeleteView(DeleteView):
    # permission_required = ('',)
    template_name = 'lists/delete_failurenode.html'
    queryset = FailureNode.objects.all()
    success_url = '/fnode/'

class RecoveryMethodDeleteView(DeleteView):
    # permission_required = ('',)
    template_name = 'lists/delete_recoverymethod.html'
    queryset = RecoveryMethod.objects.all()
    success_url = '/reco/'

# Редактирование списков
class ServiceCompanyUpdateView(UpdateView):
    # permission_required = ('',)
    template_name = 'lists/create.html'
    form_class = ServiceCompanyForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return ServiceCompany.objects.get(pk=id)

class TechniqueModelUpdateView(UpdateView):
    # permission_required = ('',)
    template_name = 'lists/create.html'
    form_class = TechniqueModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return TechniqueModel.objects.get(pk=id)

class EngineModellUpdateView(UpdateView):
    # permission_required = ('',)
    template_name = 'lists/create.html'
    form_class = EngineModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return EngineModel.objects.get(pk=id)

class TransmissionModelUpdateView(UpdateView):
    # permission_required = ('',)
    template_name = 'lists/create.html'
    form_class = TransmissionModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return TransmissionModel.objects.get(pk=id)

class DriveAxleModelUpdateView(UpdateView):
    # permission_required = ('',)
    template_name = 'lists/create.html'
    form_class = DriveAxleModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return DriveAxleModel.objects.get(pk=id)

class SteeringBridgeModelUpdateView(UpdateView):
    # permission_required = ('',)
    template_name = 'lists/create.html'
    form_class = SteeringBridgeModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return SteeringBridgeModel.objects.get(pk=id)

class ServiceTypeUpdateView(UpdateView):
    # permission_required = ('',)
    template_name = 'lists/create.html'
    form_class = ServiceTypeForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return ServiceType.objects.get(pk=id)

class FailureNodeUpdateView(UpdateView):
    # permission_required = ('',)
    template_name = 'lists/create.html'
    form_class = FailureNodeForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return FailureNode.objects.get(pk=id)

class RecoveryMethodUpdateView(UpdateView):
    # permission_required = ('',)
    template_name = 'lists/create.html'
    form_class = RecoveryMethodForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return RecoveryMethod.objects.get(pk=id)

def hello(request): #TODO убрать!!!
    return render(request, 'base.html')