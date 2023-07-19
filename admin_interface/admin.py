from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Project)
admin.site.register(projectStandard)
admin.site.register(projectPlatform)
admin.site.register(projectInterface)
admin.site.register(controllerModel)
admin.site.register(systemMedium)
admin.site.register(systemTypes)
admin.site.register(equipments)
admin.site.register(subTypeEquipments)
admin.site.register(controlTypes)
admin.site.register(signalTypes)
admin.site.register(sequenceOperation)
admin.site.register(equipmentProperties)
admin.site.register(equipmentStages)