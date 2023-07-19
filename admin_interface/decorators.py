from django.contrib.auth.models import User
from django.shortcuts import redirect


def checkIfLoginSuperAdmin(function):
	def  wrap(request, *args, **kwargs):
		loginlink = '/'
		if request.path!='/':
			loginlink += '?next=' + request.path
		print("=1=")
		if 'role' in request.session:
			userId=request.session['role']
			print('userId', userId)
			if request.session['role'] == userId:
				print("=2=")
				owner_obj = User.objects.filter(id = userId).first()
				if owner_obj:
					if request.path=='/':
						return redirect('/system/')
						# return redirect(str(settings.DASHBOARD_URL)+'dashboard/superadmin/')
				else:
					if request.path!='/':
						return redirect(loginlink)
		else:
			print("=3=")
			if request.path!='/':
				return redirect(loginlink)
		return function(request, *args, **kwargs)
	wrap.__doc__ = function.__doc__
	return wrap