import requests
import os
import json
import pandas as pd
from datetime import datetime, timedelta,date
from django.template.loader import get_template
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .states import states_dict
from .models import HospitalRegister, VaccineUpdatePost
from .forms import VaccineUpdateForm, HospitalRegisterForm, ContactUsListForm
import csv


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
		
		yesterday = date.today() - timedelta(days = 1)
		df2 = pd.read_csv('statewise_tested_numbers_data.csv',usecols=['State','Updated On','Total Tested'])
		df2['Updated On'] = pd.to_datetime(df2['Updated On'])
		newdf = (df2['Updated On'] == str(yesterday))
		newdf = df2.loc[newdf]
		newdf = newdf.reset_index().to_json(orient='records')
		newdf = json.loads(newdf)
		for nw in newdf:
			nw["TotalTested"] =nw["Total Tested"]

		Total = 0
		for total in newdf:
			if total["TotalTested"] != None:
				Total += total["TotalTested"]

		yesterday2 = date.today() - timedelta(days = 2)
		newdf2 = (df2['Updated On'] == str(yesterday2))
		newdf2 = df2.loc[newdf2]
		newdf2 = newdf2.reset_index().to_json(orient='records')
		newdf2 = json.loads(newdf2)
		for nw in newdf2:
			nw["TotalTested"] =nw["Total Tested"]

			
		print(df2)
		context = {
			
			"states": df_state,
			"india": df_india[0],
			"tested": newdf,
			"tested2": newdf2,
			"totaltested":Total
		}
		
		return render(request, "home/index.html", context)


def district_view(request, state=None, *args, **kwargs):
	state_list = {}
	state_list["Total_Testing"] = {}
	df = pd.read_csv("state_wise.csv")
	df_data = df.reset_index().to_json(orient='records')
	df_data = json.loads(df_data)

	state_data_list = []
	for state_data in df_data:
		if state_data["State_code"] == state:
			state_data_list.append(state_data)

	confirm = state_data_list[0]['Confirmed']	
	active = state_data_list[0]['Active']	
	recovered = state_data_list[0]['Recovered']	
	deaths = state_data_list[0]['Deaths']
	state2 = state_data_list[0]['State']
	
	df2 = pd.read_csv("district_wise.csv")
	df_district = df2[df2.State == state2]
	df_district = df_district.reset_index().to_json(orient='records')
	df_district_json = json.loads(df_district)

	context = {
		'confirm':confirm,
		'active':active,
		'recovered':recovered,
		'deaths':deaths,
		'state':state2,
		"alldistrict": df_district_json
		}
	return render(request, "home/district.html",context)


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