from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import requests
import datetime
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
						if "delta" in data:
							DATES.append(str(date).format(datetime.datetime.now()))
							if "confirmed" in data["delta"]:
								confirmed.append(data["delta"]["confirmed"])
							else:
								confirmed.append(0)
							if "deceased" in data["delta"]:
								deceased.append(data["delta"]["deceased"])
							else:
								deceased.append(0)
							if "other" in data["delta"]:
								other.append(data["delta"]["other"])
							else:
								other.append(0)
							if "recovered" in data["delta"]:
								recovered.append(data["delta"]["recovered"])
							else:
								recovered.append(0)
							if "tested" in data["delta"]:
								tested.append(data["delta"]["tested"])
							else:
								tested.append(0)
						if date == datetime.datetime.now().strftime("%Y-%m-%d"):
							pass
			else:
				for i, dt in dates.items():
					for date, data in dt.items():
						pass

		context = {
			"state_list": state_list,
			"confirmed": confirmed[-1],
			"deceased": deceased[-1],
			"other": other[-1],
			"recovered": recovered[-1],
			"tested": tested[-1],
			"dates": DATES,
			"active": confirmed[-1] - (recovered[-1] + deceased[-1] + other[-1]),
		}
		return render(request, "home/index.html", context)


def district_view(request, state=None, *args, **kwargs):
	try:
		chain = requests.get("https://api.covid19india.org/v4/data.json")
	except:
		return HttpResponse("<script>location.reload();</script>")

	chain = chain.json()

	districts, total, confirmed, recovered, deceased, tested = [], [], [], [], [], []
	both = {}
	for state_code, data in chain.items():
		if(state_code == state):
			for district_name, data in data["districts"].items():
				districts.append(district_name)
				total.append(data["total"])
				both[district_name] = data["total"]

	state_detail = chain[state]

	context = {
		"state_detail": state_detail,
		"districts": districts,
		"total": total,
		"both": both,
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