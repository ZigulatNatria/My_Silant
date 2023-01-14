from django.db import models

class ServiceCompany(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/servisecomp'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сервисная компания'


class TechniqueModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/modeltech'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель техники'


class EngineModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/modeleng'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель двигателя'


class TransmissionModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/modeltrans'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель трансмиссии'


class DriveAxleModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/modelaxel'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель ведущего моста'


class SteeringBridgeModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/modelsteer'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель управляемого моста'


class Machine(models.Model):
    number_machine = models.TextField(unique=True, verbose_name='Зав. № машины')
    technique_model = models.ForeignKey(TechniqueModel, verbose_name='Модель техники', on_delete=models.CASCADE)
    engine_model = models.ForeignKey(EngineModel, verbose_name='Модель двигателя', on_delete=models.CASCADE)
    engine_number = models.TextField(verbose_name='Зав. № двигателя')
    transmission_model = models.ForeignKey(TransmissionModel, verbose_name='Модель трансмиссии', on_delete=models.CASCADE)
    transmission_number = models.TextField(verbose_name='Зав. № трансмиссии')
    drive_axle_model = models.ForeignKey(DriveAxleModel, verbose_name='Модель ведущего моста', on_delete=models.CASCADE)
    drive_axle_number = models.TextField(verbose_name='Зав. № ведущего моста')
    steering_bridge_model = models.ForeignKey(SteeringBridgeModel, verbose_name='Модель управляемого моста', on_delete=models.CASCADE)
    steering_bridge_number = models.TextField(verbose_name='Зав. № управляемого моста')
    supply_contract = models.TextField(verbose_name='Договор поставки №, дата')
    shipping_date = models.DateField(verbose_name='Дата отгрузки с завода')
    consignee = models.TextField(verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.TextField(verbose_name='Адрес поставки (эксплуатации)')
    equipment = models.TextField(verbose_name='Комплектация (доп. опции)')
    client = models.TextField(verbose_name='Клиент')
    service_company = models.ForeignKey(ServiceCompany, verbose_name='Сервисная компания', on_delete=models.CASCADE)

    def get_absolute_url(self):
        # return f'/to/{self.id}'
        return f'/user'

    def __str__(self):
        return self.number_machine

    class Meta:
        verbose_name = 'Машина'
        ordering = ['-shipping_date'] # Сортировка по дате отгрузки

class ServiceType(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/servisetype'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид ТО'


class TO(models.Model):
    service_type = models.ForeignKey(ServiceType, verbose_name='Вид ТО', on_delete=models.CASCADE)
    service_date = models.DateField(verbose_name='Дата проведения ТО')
    operating_time = models.FloatField(verbose_name='Наработка, м/час')
    work_order_number = models.TextField(verbose_name='№ заказ-наряда')
    work_order_date = models.DateField(verbose_name='дата заказ-наряда')
    company_make_service = models.ForeignKey(ServiceCompany, verbose_name='Сервисная компания', on_delete=models.CASCADE)
    machine_to = models.ForeignKey(Machine, verbose_name='Зав. № машины', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'/to'

    def __str__(self):
        return self.work_order_number

    class Meta:
        verbose_name = '«ТО» (техническое обслуживание)'
        ordering = ['-service_date'] #Фильтрация по дате проведения ТО


class FailureNode(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/fnode'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характер отказа'


class RecoveryMethod(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/reco'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Способ восстановления'


class Complaint(models.Model):
    date_rejection = models.DateField(verbose_name='Дата отказа')
    operating_time = models.FloatField(verbose_name='Наработка, м/час')
    failure_node = models.ForeignKey(FailureNode, verbose_name='Узел отказа', on_delete=models.CASCADE)
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.ForeignKey(RecoveryMethod, verbose_name='Способ восстановления', on_delete=models.CASCADE)
    spare_parts = models.TextField(verbose_name='Используемые запасные части', null=True, blank=True)
    recovery_date = models.DateField(verbose_name='Дата восстановления')
    machine_complaint = models.ForeignKey(Machine, verbose_name='Зав. № машины', on_delete=models.CASCADE)
    service_company_complaint = models.ForeignKey(ServiceCompany, verbose_name='Сервисная компания', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'/complaint'

    def downtime(self):
        return (self.recovery_date - self.date_rejection).days

    def __str__(self):
        return self.failure_description

    class Meta:
        verbose_name = 'Рекламации'
        ordering = ['-date_rejection']  # Фильтрация по дате отказа

