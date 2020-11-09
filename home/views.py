from django.template.loader import get_template
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import requests
from datetime import datetime, timedelta
from .states import states_dict
from .models import HospitalRegister, VaccineUpdatePost
from .forms import VaccineUpdateForm, HospitalRegisterForm, ContactUsListForm

# Create your views here.
def home_view(request, *args, **kwargs):
	if request.method == "GET":

		try:
			chain = requests.get("https://api.covid19india.org/v4/data.json")
			timeseries = requests.get("https://api.covid19india.org/v4/timeseries.json")
		except:
			return HttpResponse("<script>location.reload();</script>")

		# extracting data in json format 
		chain = chain.json()
		timeseries = timeseries.json()

		state_list = {}
		for k, v in chain.items():
			v["code"] = k
			state_list[states_dict[k]] = v

		try:
			new_chain = requests.get("https://api.covid19india.org/v4/data-all.json")
		except:
			return HttpResponse("<script>location.reload();</script>")

		new_chain = new_chain.json()

		blank, confirmed, active, recovered, deceased = [], [], [], [], []
		for dates, states_data in new_chain.items():
			blank.append(datetime.strptime(dates, "%Y-%m-%d").strftime("%d-%b"))
			for state_code, state_data in states_data.items():
				if(state_code == "TT"):
					confirmed.append(state_data.get("total").get("confirmed", 0))
					active.append(
						state_data.get("total").get("confirmed") - 
						( state_data.get("total").get("recovered", 0) + 
							state_data.get("total").get("deceased", 0)))
					recovered.append(state_data.get("total").get("recovered", 0))
					deceased.append(state_data.get("total").get("deceased", 0))

		context = {
			"state_list": state_list,
			"blank": blank[-30:],
			"confirmed": confirmed[-30:],
			"active": active[-30:],
			"recovered": recovered[-30:],
			"deceased": deceased[-30:],
		}
		return render(request, "home/index.html", context)


def district_view(request, state=None, *args, **kwargs):

	try:
		new_chain = requests.get("https://api.covid19india.org/v4/data-all.json")
	except:
		return HttpResponse("<script>location.reload();</script>")

	new_chain = new_chain.json()

	blank, confirmed, active, recovered, deceased = [], [], [], [], []
	district_data = {}

	for dates, states_data in new_chain.items():
		blank.append(datetime.strptime(dates, "%Y-%m-%d").strftime("%d-%b"))
		for state_code, state_data in states_data.items():
			if(state_code == state):
				confirmed.append(state_data.get("total").get("confirmed", 0))
				active.append(
					state_data.get("total").get("confirmed") - 
					( state_data.get("total").get("recovered", 0) + 
						state_data.get("total").get("deceased", 0)))
				recovered.append(state_data.get("total").get("recovered", 0))
				deceased.append(state_data.get("total").get("deceased", 0))

				if(dates == datetime.today().strftime("%Y-%m-%d")):
					for district, data in state_data["districts"].items():
						district_data[district] = data["total"]
				elif(dates == (datetime.today()-timedelta(days=1)).strftime("%Y-%m-%d")):
					for district, data in state_data["districts"].items():
						district_data[district] = data["total"]


	context = {
		"state": state,
		"both": district_data,
		"blank": blank[-30:],
		"confirmed": confirmed[-30:],
		"active": active[-30:],
		"recovered": recovered[-30:],
		"deceased": deceased[-30:],
	}

	return render(request, "home/district.html", context)


def vaccine_update_view(request, *args, **kwargs):
	form = VaccineUpdateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, "You are Subscribed for Vaccination Update, We'll notify for COVID Vaccination Update")
		form = VaccineUpdateForm()
	object_list = VaccineUpdatePost.objects.all().order_by("-date_added")
	context = {
		"form": form,
		"object_list": object_list,
	}
	return render(request, "home/vaccine_update.html", context)


def hospital_register_view(request, *args, **kwargs):
	form = HospitalRegisterForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, "Your detail will be submitted after verification. You may get a call for that, Thank you !")
		form = HospitalRegisterForm()
	context = {
		"form": form,
	}
	return render(request, "home/hospital_register.html", context)


def verified_hospital_view(request, *args, **kwagrs):
	context = {
		"object_list": HospitalRegister.objects.all()
	}
	return render(request, "home/verified_hospital.html", context)


def chart_view(request, *args, **kwagrs):
	if request.method == "GET":
		try:
			chain = requests.get("https://api.covid19india.org/v4/data-all.json")
		except:
			return HttpResponse("<script>location.reload();</script>")

	chain = chain.json()

	blank, confirmed, active, recovered, deceased = [], [], [], [], []
	for dates, states_data in chain.items():
		for state_code, state_data in states_data.items():
			if(state_code == "TT"):
				confirmed.append(state_data.get("total").get("confirmed", 0))
				active.append(
					state_data.get("total").get("confirmed") - 
					( state_data.get("total").get("recovered", 0) + 
						state_data.get("total").get("deceased", 0)))
				recovered.append(state_data.get("total").get("recovered", 0))
				deceased.append(state_data.get("total").get("deceased", 0))
				blank.append("")

	context = {
		"blank": blank[-8:],
		"confirmed": confirmed[-8:],
		"active": active[-8:],
		"recovered": recovered[-8:],
		"deceased": deceased[-8:],
	}
	return render(request, "home/chart.html", context)


def contact_us_view(request, *args, **kwargs):
	form = ContactUsListForm(request.POST or None)

	if request.method == "POST":
		if form.is_valid():
			form.save()
			messages.success(request, "Your Response has Successfully Submitted")
			form = ContactUsListForm()

	context = {
		"form": form,
	}
	return render(request, "contact-us.html", context)