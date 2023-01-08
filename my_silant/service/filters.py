from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Machine, TO, Complaint


# создаём фильтр
class MachineFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Machine
        fields = (
            # 'number_machine',
            # 'technique_model',
            # 'engine_model',
            # 'engine_number',
            # 'transmission_model',
            # 'transmission_number',
            # 'drive_axle_model',
            # 'drive_axle_number',
            # 'steering_bridge_model',
            # 'steering_bridge_number',
            '__all__'
        )  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)


class TOFilter(FilterSet):

    class Meta:
        model = TO
        fields = (
            'service_type',
            'service_date',
            'operating_time',
            'work_order_number',
            'work_order_date',
            'company_make_service',
            'machine_to',
        )


class ComplaintFilter(FilterSet):

    class Meta:
        model = Complaint
        fields =(
            'date_rejection',
            'operating_time',
            'failure_node',
            'failure_description',
            'recovery_method',
            'spare_parts',
            'recovery_date',
            'machine_complaint',
            'service_company_complaint',
        )