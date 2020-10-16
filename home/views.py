from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import requests
from .states import states_dict
from .models import HospitalRegister, VaccineUpdatePost
from .forms import VaccineUpdateForm, HospitalRegisterForm

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


		confirmed, deceased, other, recovered, tested, DATES = [], [], [], [], [], []
		for st, dates in timeseries.items():
			if st == "TT":
				for i, dt in dates.items():
					for date, data in dt.items():
						DATES.append(date)
						if "delta" in data:
							if "confirmed" in data["delta"]:
								# confirmed[date] = data["delta"]["confirmed"]
								confirmed.append(data["delta"]["confirmed"])
							# if "deceased" in data["delta"]:
							# 	deceased[date] = data["delta"]["deceased"]
							# if "other" in data["delta"]:
							# 	other[date] = data["delta"]["other"]
							# if "recovered" in data["delta"]:
							# 	recovered[date] = data["delta"]["recovered"]
							# if "tested" in data["delta"]:
							# 	tested[date] = data["delta"]["tested"]
		# print(DATES)
		# print(len(DATES))
		context = {
			"state_list": state_list,
			# "timeseries": timeseries,
			"confirmed": confirmed,
			"deceased": deceased,
			"other": other,
			"recovered": recovered,
			"tested": tested,
			"dates": DATES,
		}
		return render(request, "home/index.html", context)


def district_view(request, state=None, *args, **kwargs):
	try:
		chain = requests.get("https://api.covid19india.org/v4/data.json")
	except:
		return HttpResponse("<script>location.reload();</script>")

	chain = chain.json()

	state_detail = chain[state]

	context = {
		"state_detail": state_detail,
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
		messages.success(request, "Your Detail Has been Updated, You may get a Call for Cofirmation, After Confirmation Your Information will be on Site at COVID Hospital List")
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