from django.forms import ModelForm
from .models import TO, Complaint, Machine

class TOForm(ModelForm):

    class Meta:
        model = TO
        fields = [
            'service_type',
            'service_date',
            'operating_time',
            'work_order_number',
            'work_order_date',
            'company_make_service',
            'machine_to',
        ]


class ComplaintForm(ModelForm):

    class Meta:
        model = Complaint
        fields = [
            'date_rejection',
            'operating_time',
            'failure_node',
            'failure_description',
            'recovery_method',
            'spare_parts',
            'recovery_date',
            'machine_complaint',
        ]

class MachineForm(ModelForm):

    class Meta:
        model = Machine
        fields = [
            'number_machine',
            'technique_model',
            'engine_model',
            'engine_number',
            'transmission_model',
            'transmission_number',
            'drive_axle_model',
            'drive_axle_number',
            'steering_bridge_model',
            'steering_bridge_number',
            'supply_contract',
            'shipping_date',
            'delivery_address',
            'equipment',
            'client',
            'service_company',
        ]

