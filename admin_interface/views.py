from django.http import JsonResponse
from django.shortcuts import render ,HttpResponse, redirect
from .models import *
from django.views.generic import TemplateView
from django.views import View
from django.db.models import Q
from . import forms
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from .decorators import *
# Create your views here.


@method_decorator(checkIfLoginSuperAdmin, name="dispatch")
class check(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, *args, **kwargs):
		context = super(check, self).get_context_data()
		context['standard'] = projectStandard.objects.all()
		context['platform'] = projectPlatform.objects.all()
		context['interface'] = projectInterface.objects.all()
		context['controller'] = controllerModel.objects.all()
		context['systeMedium'] = systemMedium.objects.all()
		context['signalTypes'] = signalTypes.objects.all()
		context['allProject'] = Project.objects.all()
		if 'main_id' in self.request.GET:
			context['systemType'] = systemTypes.objects.filter(sysMedium=self.request.GET.get('main_id')).all()
			context['equipments'] = equipments.objects.filter(sysMedium=self.request.GET.get('main_id')).all()
			context['controltype'] = controlTypes.objects.filter(sysMedium=self.request.GET.get('main_id')).all()
			print(context['systemType'])
		if 'equip_id' in self.request.GET:
			print('id', self.request.GET)
			context['subTypeEquip'] = subTypeEquipments.objects.filter(equipmentId=self.request.GET.get('equip_id')).all()
		return context

	def post(self, request):
		form = forms.addSystem(request.POST)
		if form.is_valid():
			print('formisValid')
			project_number = form.cleaned_data.get('project_number')
			project_name = form.cleaned_data.get('project_name')
			standard = form.cleaned_data.get('standard')
			system_tag = form.cleaned_data.get('system_tag')
			platform = form.cleaned_data.get('platform')
			interface = form.cleaned_data.get('interface')
			controller = form.cleaned_data.get('controller')
			system_medium = form.cleaned_data.get('system_medium')
			system_type = form.cleaned_data.get('system_type')
			equip_sec = form.cleaned_data.get('equip_sec')
			sequence_data = form.cleaned_data.get('sequence_data')

			all_data = json.loads(equip_sec) if equip_sec else {}
			copy_list = all_data[:]
			for idx, data in enumerate(copy_list):
				if data['property'] == []:
					del all_data[idx]

			equip_sec = json.dumps(all_data)



			standard_id = projectStandard.objects.filter(id=standard).first()
			platform_id = projectPlatform.objects.filter(id=platform).first()
			interface_id = projectInterface.objects.filter(id=interface).first()
			controller_id = controllerModel.objects.filter(id=controller).first()
			system_medium_id = systemMedium.objects.filter(id=system_medium).first()
			system_type_id = systemTypes.objects.filter(id=system_type).first()
			projectObj = Project.objects.create(projectNumber=project_number, projectName=project_name,
												standard=standard_id, systemTag=system_tag, platform=platform_id, interface=interface_id,
												controller=controller_id, sysmedium=system_medium_id, systype=system_type_id,)
			projectObj.equipmentsection=equip_sec
			projectObj.save()
			if projectObj:
				sequenceOperation.objects.create(projectId=projectObj, sequence=sequence_data)
				equipmetData = equip_sec
				if equipmetData:
					js = json.loads(equipmetData)
					for i in range(len(js)):
						equipmet_id = js[i]['equipmentId']
						control_id = js[i]['controlTypeId']				
						equipId = equipments.objects.get(id=equipmet_id)
						equipment_property = equipmentProperties.objects.create(projectId=projectObj, equipmentId=equipId)
						if control_id:
							contrId = controlTypes.objects.get(id=control_id)
							equipment_property.controlId = contrId
							equipment_property.save()
						properties = js[i]['property']
						print(len(properties))
						for prop in range(len(properties)):
							count = properties[prop]['count']
							stage_type = properties[prop]['stage']
							signal_type = properties[prop]['signalType']
							# if signal_type: equipment_stages.signalType = signalTypes.objects.get(id=signal_type)
							equipment_stages = equipmentStages.objects.create(
								stageType=subTypeEquipments.objects.get(id=stage_type) if stage_type else None,
								equipPropertyId=equipment_property,
								signalType=signalTypes.objects.get(id=signal_type) if signal_type else None,
								stageCount=count)
							# if stage_type:
							# 	equipment_stages.stageType = subTypeEquipments.objects.get(id=stage_type)
							equipment_stages.save()
			return redirect('/system/')
		else:
			return render(request, self.template_name, {'form': form})


def check_controller(request):
	text = request.GET.get('controller')
	print(type(text))
	post = controllerModel.objects.filter(Q(controller=text)).first()
	if post:
		return JsonResponse({'status': 200})
	else:
		message = 'This value does not exist in our database'
		return JsonResponse(message, safe=False)
		

class loginAdmin(TemplateView):
	template_name = 'login.html'

	def get(self, request):
		return render(request, self.template_name, {})

	def post(self, request):
		form = forms.login(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			print('user', user)
			if user:
				print('1213')
				login(request, user)
				print('3232')
				request.session['role'] = user.id
				request.session.save()
				# messages.success(request, "Welcome")
				return redirect('/system/')
			else:
				messages.error(request, "Invalid username or password.")
				return render(request, 'login.html')
		else:
			return render(request, self.template_name, {'form': form})


@method_decorator(checkIfLoginSuperAdmin, name="dispatch")
class Logout(LoginRequiredMixin, TemplateView):
	template_name = 'login.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_superuser:
			logout(request)
			messages.success(request, "Logout Successful")
			return redirect('/')
		return redirect('/')


@method_decorator(checkIfLoginSuperAdmin, name="dispatch")
class getSubEquipment(APIView):
	def get(self, request):
		try:
			allData = []
			data = request.data
			print('sd')
			equipmentss= request.GET['equipmentid']
			if not equipmentss:
				return JsonResponse({"status_code": '400', "status_message": 'equipment id required'})
			equipmentObj = equipments.objects.filter(id=equipmentss).first()
			print('equipmentObj', equipmentObj)
			if not equipmentObj:
				return JsonResponse({"status_code": '400', "status_message": 'equipment id invalid'})
			subEquipmentObj = subTypeEquipments.objects.filter(equipmentId=equipmentObj)
			print('subEquipmentObj', subEquipmentObj)
			for i in subEquipmentObj:
				data = {
					'equipment': i.equipmentId.id,
					'subEquipmentId': i.id,
					'subEquipment': i.subEquipment
				}
				allData.append(data)
			return JsonResponse({'data': allData})
		except Exception as e:
			return JsonResponse({"status_code": '500', "status_message": str(e)})
# old search functyionality
# @method_decorator(checkIfLoginSuperAdmin,name="dispatch")
# class searchFilter(APIView):
# 	def get(self,request):
# 		try:
# 			data = request.data
# 			allData = []
# 			data = {}
# 			search_value = request.GET.get('para','')
# 			print('search_value',search_value)
# 			if not search_value:
# 				return JsonResponse({"status_code":'400',"status_message":'para id required'}) 
# 			sequence_data = sequenceOperation.objects.filter(sequence__icontains=search_value)
# 			projectDetail = Project.objects.filter(Q(projectNumber__icontains=search_value) | Q(projectName__icontains=search_value))
# 			if projectDetail:
# 				print('projectDetail')
# 				for i in projectDetail:
# 					data = {
# 					'projectId':i.id,
# 					'projectNumber':i.projectNumber,
# 					'systemTag':i.systemTag,
# 					}
# 					allData.append(data)
# 			if sequence_data:
# 				print('sequence_data')
# 				for i in sequence_data:
# 					data = {
# 					'projectId':i.projectId.id,
# 					'projectNumber':i.projectId.projectNumber,
# 					'systemTag':i.projectId.systemTag,
# 					}
# 					allData.append(data)
# 			return JsonResponse({'data':allData})
# 		except Exception as e:
# 			return JsonResponse({"status_code":'500',"status_message":str(e)})


@method_decorator(checkIfLoginSuperAdmin,name="dispatch")
class EditSystem(TemplateView):
	template_name = 'edit-system.html'

	def get(self, request, id):
		data = Project.objects.filter(id=id).first()
		sequence_data = sequenceOperation.objects.filter(projectId=data).first()
		standard = projectStandard.objects.all()
		platform = projectPlatform.objects.all()
		interface = projectInterface.objects.all()
		controller = controllerModel.objects.all()
		systeMedium= systemMedium.objects.all()
		signalType = signalTypes.objects.all()
		if 'main_id' in self.request.GET:
			systemType = systemTypes.objects.filter(sysMedium=self.request.GET.get('main_id')).all()
			equipment = equipments.objects.filter(sysMedium=self.request.GET.get('main_id')).all()
			controltype = controlTypes.objects.filter(sysMedium=self.request.GET.get('main_id')).all()
		if 'equip_id' in self.request.GET:
			subTypeEquip = subTypeEquipments.objects.filter(equipmentId=self.request.GET.get('equip_id')).all()
		return render(request, self.template_name, locals())
	
	def post(self, request, id):
		form = forms.addSystem(request.POST)
		if form.is_valid():
			project_number = form.cleaned_data.get('project_number')
			project_name = form.cleaned_data.get('project_name')
			standard = form.cleaned_data.get('standard')
			system_tag = form.cleaned_data.get('system_tag')
			platform = form.cleaned_data.get('platform')
			interface = form.cleaned_data.get('interface')
			controller = form.cleaned_data.get('controller')
			system_medium = form.cleaned_data.get('system_medium')
			system_type = form.cleaned_data.get('system_type')
			equip_sec = form.cleaned_data.get('equip_sec')
			sequence_data = form.cleaned_data.get('sequence_data')
			standard_id = projectStandard.objects.filter(id=standard).first()
			platform_id = projectPlatform.objects.filter(id=platform).first()
			interface_id = projectInterface.objects.filter(id=interface).first()
			controller_id = controllerModel.objects.filter(id=controller).first()
			system_medium_id = systemMedium.objects.filter(id=system_medium).first()
			system_type_id = systemTypes.objects.filter(id=system_type).first()
			projectObj = Project.objects.filter(id=id).first()
			projectObj.platform = platform_id
			projectObj.interface = interface_id
			projectObj.controller = controller_id
			projectObj.sysmedium = system_medium_id
			projectObj.systype = system_type_id
			projectObj.equipmentsection = equip_sec
			projectObj.save()
			sequenceObj = sequenceOperation.objects.filter(projectId=projectObj).first()
			sequenceObj.sequence = sequence_data
			sequenceObj.save()
			equipmetData = equip_sec
			if equipmetData:
				js = json.loads(equipmetData)
				for i in range(len(js)):
					equipmet_id = js[i]['equipmentId']
					control_id = js[i]['controlTypeId']
					equipId = equipments.objects.get(id=equipmet_id)
					equipment_property = equipmentProperties.objects.filter(projectId=projectObj, equipmentId=equipId).first()
					if not equipment_property:
						equipment_property = equipmentProperties.objects.create(projectId=projectObj,equipmentId=equipId)
					if control_id:
						contrId = controlTypes.objects.get(id=control_id)
						equipment_property.controlId=contrId
						equipment_property.save()
					properties = js[i]['property']
					print(len(properties))
					for prop in range(len(properties)):
						count = properties[prop]['count']
						stage_type = properties[prop]['stage']
						signal_type = properties[prop]['signalType']
						equipment_stages = equipmentStages.objects.filter(equipPropertyId=equipment_property,stageCount=count).first()
						if not equipment_stages:
							equipment_stages = equipmentStages.objects.create(equipPropertyId=equipment_property,stageCount=count)
						if stage_type: equipment_stages.stageType = subTypeEquipments.objects.get(id=stage_type)
						if signal_type: equipment_stages.signalType = signalTypes.objects.get(id=signal_type)
						equipment_stages.save()
			return redirect('/system/')
		else:
			return render(request, self.template_name, {'form': form})


@method_decorator(checkIfLoginSuperAdmin, name="dispatch")
class deleteSystem(View):
	def get(self, request, id):
		Project.objects.filter(id=id).delete()
		return redirect('/system/')


# @method_decorator(checkIfLoginSuperAdmin,name="dispatch")
class searchFilter(APIView):
	def get(self, request):
		try:
			# data = request.data
			data = request.GET
			allData = []
			project_number = data.get('project_number')
			project_name = data.get('project_name')
			standard_value = data.get('standard_id')
			system_tag = data.get('system_tag')
			platform_value = data.get('platform_id')
			interface_value = data.get('interface_id')
			controller_value = data.get('controller_id')
			medium_value = data.get('medium_id')
			systype_value = data.get('systemtype_id')
			sequence_value = data.get('sequence_operation')
			equipment_value = data.get('equipment_id')
			control_value = data.get('control_id')
			equipment_section = data.get('equipment_section')
			lookups = Q()
			if project_number:
				lookups.add(Q(projectNumber__icontains=project_number), Q.AND)
			if project_name:
				lookups.add(Q(projectName__icontains=project_name), Q.AND)
			if standard_value:
				lookups.add(Q(standard=standard_value), Q.AND)
			if system_tag:
				lookups.add(Q(systemTag__icontains=system_tag), Q.AND)
			if platform_value:
				lookups.add(Q(platform=platform_value), Q.AND)
			if interface_value:
				lookups.add(Q(interface=interface_value), Q.AND)
			if controller_value:
				lookups.add(Q(controller=controller_value), Q.AND)
			if medium_value:
				lookups.add(Q(sysmedium=medium_value), Q.AND)
			if systype_value:
				lookups.add(Q(systype=systype_value), Q.AND)
			if sequence_value:
				lookups.add(Q(sequenceoperation__sequence__icontains=sequence_value), Q.AND)
			if equipment_value:
				lookups.add(Q(equipmentproperties__equipmentId__equipment__icontains=equipment_value), Q.AND)
			if control_value:
				lookups.add(Q(equipmentproperties__controlId=control_value), Q.AND)
			import json
			all_data = json.loads(equipment_section) if equipment_section else {}
			if equipment_section:

				for data in all_data:
					is_first = True
					result = ''
					if data['controlTypeId'] is None and data['property'] == []:
						for key, value in data.items():
							if key not in ('controlTypeId', 'property'):
								if value is not None:
									# todo: space issue fix kerna hai.
									if is_first:
										result += f'"{key}": "{value}",'
										is_first = False
									else:
										result += f' "{key}": "{value}",'
						lookups.add(Q(equipmentsection__icontains=result), Q.AND)
					elif data['controlTypeId'] is not None:
						for key, value in data.items():
							if key != 'property':
								if value is not None:
									if is_first:
										result += f'"{key}": "{value}",'
										is_first = False
									else:
										result += f' "{key}": "{value}",'
						lookups.add(Q(equipmentsection__icontains=result), Q.AND)


			projectDetail = Project.objects.filter(lookups)
			print("projectDetail", projectDetail)
			if projectDetail:
				print('projectDetail')
				for i in projectDetail:
					match = True
					if all_data:
						for req_data in all_data:
							equi_data = json.loads(i.equipmentsection)
							for db_equip in equi_data:
								if req_data['equipmentId'] == db_equip['equipmentId']:
									if (req_data["property"] != [] and db_equip['property'] != []) and len(req_data["property"]) == len(db_equip['property']):
										for j in range(len(req_data["property"])):
											if req_data["property"][j]['stage'] is not None and req_data["property"][j]['stage'] == db_equip["property"][j]['stage']:
												match = True
											elif req_data["property"][j]['stage'] is None:
												match = True
											else:
												match = False

											if req_data["property"][j]['signalType'] is not None and \
													req_data["property"][j]['signalType'] == db_equip["property"][j][
												'signalType']:
												match = True
											elif req_data["property"][j]['signalType'] is None:
												match = True
											else:
												match = False
									elif req_data["property"] == [] and db_equip['property'] == []:
										match = True
									elif req_data["property"] == [] and db_equip['property'] != []:
										match = True
									else:
										match = False
							if match == False:
								break


					if match:
						p_data = {
							'projectId': i.id,
							'projectName': i.projectName,
							'projectNumber': i.projectNumber,
							'systemTag': i.systemTag,
						}
						allData.append(p_data)
					# equip = i.equipmentsection[-45:-34]
					#
					# if not equipment_section or (data[0]['controlTypeId'] is None and data[0]['property'] == []) or\
					# 							(data[0]['controlTypeId'] is not None and data[0]['property'] == []):
					# 	p_data = {
					# 	'projectId':i.id,
					# 	'projectNumber':i.projectNumber,
					# 	'systemTag':i.systemTag,
					# 	}
					# 	allData.append(p_data)
					#
					# elif equip == stage:

			return JsonResponse({'data': allData})
		except Exception as e:
			return JsonResponse({"status_code": '500', "status_message": str(e)})



mysql = [
	{
		"equipmentId": "2",
		"equipmentName": "Exhaust Fan",
		"controlTypeId": "2",
		"property": [
			{"id": 1, "count": "Stage 1(S1)", "stage": "2", "signalType": "1"},
			{"id": 2, "count": "Stage 2(S2)", "stage": "2", "signalType": "2"},
			{"id": 3, "count": "Stage 3(S3)", "stage": "2", "signalType": "3"},
			{"id": 4, "count": "Stage 4(S4)", "stage": "2", "signalType": "1"},
			{"id": 5, "count": "Stage 5(S5)", "stage": "2", "signalType": "2"}
		]
},
    {
	 "equipmentId": "1",
	 "equipmentName": "Supply Fan",
	 "controlTypeId": "1",
	 "property":
		 [
			 {"id": 1, "count": "Stage 1(S1)", "stage": "1", "signalType": "1"}
		 ]
 }

]


# response from request
web_resp = [
	{
		"equipmentId": "1",
		"equipmentName": "Supply Fan",
		"controlTypeId": "1",
		"property": [
			{
				"id": 1,
				"count": "Stage 1(S1)",
				"stage": None,
				"signalType": 1
			}
		]
	},
	{
		"equipmentId": "2",
		"equipmentName": "Exhaust Fan",
		"controlTypeId": "1",
		"property": []
	}
]



[{"equipmentId": "1", "equipmentName": "Supply Fan", "controlTypeId": "1", "property": [{"id": 1, "count": "Stage 1(S1)", "stage": "1", "signalType": "1"}, {"id": 2, "count": "Stage 2(S2)", "stage": "1", "signalType": "2"}]}]
