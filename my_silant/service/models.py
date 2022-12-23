from django.db import models

# Create your models here.
class Machine(models.Model):
    number_machine = models.TextField(unique=True, verbose_name='Зав. № машины')
    technique_model = models.TextField(verbose_name='Модель техники') #TODO добавить справочник
    engine_model = models.TextField(verbose_name='Модель двигателя') #TODO добавить справочник
    engine_number = models.TextField(verbose_name='Зав. № двигателя')
    transmission_model = models.TextField(verbose_name='Модель трансмиссии') #TODO добавить справочник
    transmission_number = models.TextField(verbose_name='Зав. № трансмиссии')
    drive_axle_model = models.TextField(verbose_name='Модель ведущего моста') #TODO добавить справочник
    drive_axle_number = models.TextField(verbose_name='Зав. № ведущего моста')
    steering_bridge_model = models.TextField(verbose_name='Модель управляемоо моста')  #TODO добавить справочник
    steering_bridge_number = models.TextField(verbose_name='Зав. № управляемоо моста')
    supply_contract = models.TextField(verbose_name='Договор поставки №, дата')
    shipping_date = models.DateField(verbose_name='Дата отгрузки с завода') #TODO календарь
    consignee = models.TextField(verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.TextField(verbose_name='Адрес поставки (эксплуатации)')
    equipment = models.TextField(verbose_name='Комплектация (доп. опции)')
    client = models.TextField(verbose_name='Клиент') #TODO справочник пользователей с соответствующими правами
    service_company = models.TextField(verbose_name='Сервисная компания') #TODO справочник пользователей с соответствующими правами

    class Meta:
        verbose_name = 'Машина'


class TO(models.Model):
    service_type = models.TextField(verbose_name='Вид ТО') #TODO добавить справочник
    service_date = models.DateField(verbose_name='Дата проведения ТО') #TODO календарь
    operating_time = models.FloatField(verbose_name='Наработка, м/час')
    work_order_number = models.TextField(verbose_name='№ заказ-наряда')
    work_order_date = models.DateField(verbose_name='дата заказ-наряда')  # TODO календарь
    company_make_service = models.TextField(verbose_name='Организация, проводившая ТО') #TODO добавить справочник
    machine_to = models.ForeignKey(Machine, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '«ТО» (техническое обслуживание)'


class Complaint(models.Model):
    date_rejection = models.DateField(verbose_name='Дата отказа') #TODO календарь
    operating_time = models.FloatField(verbose_name='Наработка, м/час')
    failure_node = models.TextField(verbose_name='Узел отказа') #TODO добавить справочник
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.TextField(verbose_name='Способ восстановления') #TODO добавить справочник
    spare_parts = models.TextField(verbose_name='Используемые запасные части')
    recovery_date = models.DateField(verbose_name='Дата восстановления') #TODO календарь
    # downtime = models.ImageField(recovery_date - date_rejection, verbose_name='Время простоя техники')
    machine_complaint = models.ForeignKey(Machine, on_delete=models.CASCADE)

    def downtime(self):
        return (self.recovery_date - self.date_rejection).days

    class Meta:
        verbose_name = 'Рекламации'

