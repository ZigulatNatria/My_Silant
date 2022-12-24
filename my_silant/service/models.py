from django.db import models

class ServiceCompany(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сервисная компания'


class TechniqueModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель техники'


class EngineModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель двигателя'


class TransmissionModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель трансмиссии'


class DriveAxleModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель ведущего моста'


class SteeringBridgeModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель управляемого моста'


class Machine(models.Model):
    number_machine = models.TextField(unique=True, verbose_name='Зав. № машины')
    technique_model = models.OneToOneField(TechniqueModel, verbose_name='Модель техники', on_delete=models.CASCADE)
    engine_model = models.OneToOneField(EngineModel, verbose_name='Модель двигателя', on_delete=models.CASCADE)
    engine_number = models.TextField(verbose_name='Зав. № двигателя')
    transmission_model = models.OneToOneField(TransmissionModel, verbose_name='Модель трансмиссии', on_delete=models.CASCADE)
    transmission_number = models.TextField(verbose_name='Зав. № трансмиссии')
    drive_axle_model = models.OneToOneField(DriveAxleModel, verbose_name='Модель ведущего моста', on_delete=models.CASCADE)
    drive_axle_number = models.TextField(verbose_name='Зав. № ведущего моста')
    steering_bridge_model = models.OneToOneField(SteeringBridgeModel, verbose_name='Модель управляемого моста', on_delete=models.CASCADE)
    steering_bridge_number = models.TextField(verbose_name='Зав. № управляемого моста')
    supply_contract = models.TextField(verbose_name='Договор поставки №, дата')
    shipping_date = models.DateField(verbose_name='Дата отгрузки с завода') #TODO календарь
    consignee = models.TextField(verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.TextField(verbose_name='Адрес поставки (эксплуатации)')
    equipment = models.TextField(verbose_name='Комплектация (доп. опции)')
    client = models.TextField(verbose_name='Клиент') #TODO справочник пользователей с соответствующими правами
    # service_company = models.TextField(verbose_name='Сервисная компания') #TODO справочник пользователей с соответствующими правами
    service_company = models.ForeignKey(ServiceCompany, verbose_name='Сервисная компания', on_delete=models.CASCADE)

    def __str__(self):
        return self.number_machine

    class Meta:
        verbose_name = 'Машина'

class ServiceType(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид ТО'


class TO(models.Model):
    service_type = models.OneToOneField(ServiceType, verbose_name='Вид ТО', on_delete=models.CASCADE)
    service_date = models.DateField(verbose_name='Дата проведения ТО') #TODO календарь
    operating_time = models.FloatField(verbose_name='Наработка, м/час')
    work_order_number = models.TextField(verbose_name='№ заказ-наряда')
    work_order_date = models.DateField(verbose_name='дата заказ-наряда')  # TODO календарь
    company_make_service = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE)
    # company_make_service = models.TextField(verbose_name='Организация, проводившая ТО') #TODO добавить справочник
    machine_to = models.ForeignKey(Machine, on_delete=models.CASCADE)

    def __str__(self):
        return self.work_order_number

    class Meta:
        verbose_name = '«ТО» (техническое обслуживание)'


class FailureNode(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характер отказа'


class RecoveryMethod(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Способ восстановления'


class Complaint(models.Model):
    date_rejection = models.DateField(verbose_name='Дата отказа') #TODO календарь
    operating_time = models.FloatField(verbose_name='Наработка, м/час')
    failure_node = models.OneToOneField(FailureNode, verbose_name='Узел отказа', on_delete=models.CASCADE)
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.OneToOneField(RecoveryMethod, verbose_name='Способ восстановления', on_delete=models.CASCADE)
    spare_parts = models.TextField(verbose_name='Используемые запасные части')
    recovery_date = models.DateField(verbose_name='Дата восстановления') #TODO календарь
    machine_complaint = models.ForeignKey(Machine, on_delete=models.CASCADE)

    def downtime(self):
        return (self.recovery_date - self.date_rejection).days

    def __str__(self):
        return self.failure_description

    class Meta:
        verbose_name = 'Рекламации'

