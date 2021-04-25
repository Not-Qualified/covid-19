import requests
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from django.template.loader import get_template
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .states import states_dict
from .models import HospitalRegister, VaccineUpdatePost
from .forms import VaccineUpdateForm, HospitalRegisterForm, ContactUsListForm

# Create your views here.
def home_view(request, *args, **kwargs):
	if request.method == "GET":
		state_list = {}

		df = pd.read_csv("state_wise.csv", )
		df_state = df[(df.State != "Total") & (df.State != "State Unassigned")]
		df_state = df_state.reset_index().to_json(orient='records')
		df_state = json.loads(df_state)

		df_india = df[df.State == "Total"]
		df_india = df_india.reset_index().to_json(orient='records')
		df_india = json.loads(df_india)

		
		# print(type(data), data)
		# print(df_all)

		context = {
			# "state_list": state_list,
			# "blank": blank[-30:],
			# "confirmed": confirmed[-30:],
			# "active": active[-30:],
			# "recovered": recovered[-30:],
			# "deceased": deceased[-30:],
			# "district": district_confirmed,
			"states": df_state,
			"india": df_india[0],
		}
		return render(request, "home/index.html", context)


def district_view(request, state=None, *args, **kwargs):
	state_list = {}
	state_list["Total_Testing"] = {}

	# try:
	# 	new_chain = requests.get("https://api.covid19india.org/v4/data-all.json")
	# except:
	# 	return HttpResponse("<script>location.reload();</script>")

	# new_chain = new_chain.json()

	with open('/opt/data-all.json') as f:
			new_chain = json.load(f)
			f.close()

	blank, confirmed, active, recovered, deceased = [], [], [], [], []
	district_data = {}

	for dates, states_data in new_chain.items():
		blank.append(datetime.strptime(dates, "%Y-%m-%d").strftime("%d-%b"))
		for state_code, state_data in states_data.items():
			if(state_code == state):
				state_list["Total_Testing"]["total"] = state_data.get("total")

				confirmed.append(state_data.get("total").get("confirmed", 0))
				active.append(
					state_data.get("total").get("confirmed", 0) - 
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


	state = states_dict.get(state, "")
	context = {
		"state": state,
		"both": district_data,
		"state_list": state_list,
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