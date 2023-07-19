from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

# class Project(models.Model):
# 	projectNumber = models.CharField(max_length=50,null=True,blank=True,default='')
# 	projectName =  models.CharField(max_length=50,null=True,blank=True,default='')
# 	standard = models.CharField(max_length=50,null=True,blank=True,default='')
# 	systemTag = models.CharField(max_length=50,null=True,blank=True,default='')
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)


# 	def __str__(self):
# 		return str(self.projectName)

class projectStandard(models.Model):
	standard = models.CharField(max_length=50,null=True,blank=True,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return str(self.standard)


class projectPlatform(models.Model):
	platform = models.CharField(max_length=50,null=True,blank=True,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.platform)

class projectInterface(models.Model):
	interface = models.CharField(max_length=50,null=True,blank=True,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.interface)

class controllerModel(models.Model):
	controller = models.CharField(max_length=50,null=True,blank=True,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.controller)


class systemMedium(models.Model):
	systemMediumType = models.CharField(max_length=50,null=True,blank=True,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return str(self.systemMediumType)


class systemTypes(models.Model):
	sysMedium = models.ForeignKey(systemMedium,on_delete=models.CASCADE)
	systemType = models.CharField(max_length=50,null=True,blank=True,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.systemType)


class equipments(models.Model):
	sysMedium = models.ForeignKey(systemMedium,on_delete=models.CASCADE)
	equipment = models.CharField(max_length=50,null=True,blank=True,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.equipment)


class subTypeEquipments(models.Model):
	equipmentId = models.ForeignKey(equipments,on_delete=models.CASCADE)
	subEquipment = models.CharField(max_length=50,null=True,blank=True,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.subEquipment)


class controlTypes(models.Model):
	sysMedium = models.ForeignKey(systemMedium,on_delete=models.CASCADE)
	controlType = models.CharField(max_length=50,null=True,blank=True,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.controlType)


class signalTypes(models.Model):
	signalType = models.CharField(max_length=50,null=True,blank=True,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.signalType)
	
class Project(models.Model):
	projectNumber = models.CharField(max_length=50,null=True,blank=True,default='')
	projectName = models.CharField(max_length=50,null=True,blank=True,default='')
	standard = models.ForeignKey(projectStandard,on_delete=models.CASCADE)
	systemTag = models.CharField(max_length=50,null=True,blank=True,default='')
	platform = models.ForeignKey(projectPlatform,on_delete=models.CASCADE)
	interface = models.ForeignKey(projectInterface,on_delete=models.CASCADE)
	controller = models.ForeignKey(controllerModel,on_delete=models.CASCADE)
	sysmedium = models.ForeignKey(systemMedium,on_delete=models.CASCADE)
	systype = models.ForeignKey(systemTypes,on_delete=models.CASCADE)
	equipmentsection = models.TextField(blank=True)
	# equipmentproperty = models.TextField(blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.projectName)


class equipmentProperties(models.Model):
	projectId = models.ForeignKey(Project,on_delete=models.CASCADE)
	equipmentId = models.ForeignKey(equipments,on_delete=models.CASCADE)
	controlId = models.ForeignKey(controlTypes,on_delete=models.CASCADE,null=True,blank=True)
	data = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.projectId.projectNumber)


class equipmentStages(models.Model):
	equipPropertyId = models.ForeignKey(equipmentProperties, on_delete=models.CASCADE)
	stageCount = models.CharField(max_length=20, null=True, blank=True, default='')
	stageType = models.ForeignKey(subTypeEquipments, on_delete=models.CASCADE)
	signalType = models.ForeignKey(signalTypes, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.equipPropertyId.id)


class sequenceOperation(models.Model):
	projectId = models.ForeignKey(Project,on_delete=models.CASCADE)
	sequence = RichTextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
