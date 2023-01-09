from django.forms import ModelForm
from .models import TO, Complaint, Machine
from .models import *

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
            'service_company_complaint',
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

# Формы списков
class ServiceCompanyForm(ModelForm):

    class Meta:
        model = ServiceCompany
        fields = [
            'name',
            'description',
        ]

class TechniqueModelForm(ModelForm):

    class Meta:
        model = TechniqueModel
        fields = [
            'name',
            'description',
        ]

class EngineModelForm(ModelForm):

    class Meta:
        model = EngineModel
        fields = [
            'name',
            'description',
        ]

class TransmissionModelForm(ModelForm):

    class Meta:
        model = TransmissionModel
        fields = [
            'name',
            'description',
        ]

class DriveAxleModelForm(ModelForm):

    class Meta:
        model = DriveAxleModel
        fields = [
            'name',
            'description',
        ]

class SteeringBridgeModelForm(ModelForm):

    class Meta:
        model = SteeringBridgeModel
        fields = [
            'name',
            'description',
        ]

class ServiceTypeForm(ModelForm):

    class Meta:
        model = ServiceType
        fields = [
            'name',
            'description',
        ]

class FailureNodeForm(ModelForm):

    class Meta:
        model = FailureNode
        fields = [
            'name',
            'description',
        ]

class RecoveryMethodForm(ModelForm):

    class Meta:
        model = RecoveryMethod
        fields = [
            'name',
            'description',
        ]