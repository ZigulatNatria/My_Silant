from django.contrib import admin
from .models import Machine, TO, Complaint
#Модели справочников
from .models import ServiceCompany, TechniqueModel, EngineModel, TransmissionModel, \
    DriveAxleModel, SteeringBridgeModel, ServiceType, FailureNode, RecoveryMethod
# Register your models here.
admin.site.register(Machine)
admin.site.register(TO)
admin.site.register(Complaint)

# Модели справочников
admin.site.register(ServiceCompany)
admin.site.register(TechniqueModel)
admin.site.register(TransmissionModel)
admin.site.register(DriveAxleModel)
admin.site.register(SteeringBridgeModel)
admin.site.register(ServiceType)
admin.site.register(FailureNode)
admin.site.register(RecoveryMethod)
admin.site.register(EngineModel)
