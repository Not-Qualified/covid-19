from django import forms
from .models import (VaccineUpdate, 
					HospitalRegister, )

# Registering Forms

DISTRICT_CHOICES = [("", "Select District"), ]

STATE_CHOICES = [
	("", "Select State"),
	("Andaman Nicobar", "Andaman Nicobar"), 
	("Andhra Pradesh", "Andhra Pradesh"), 
	("Arunachal Pradesh", "Arunachal Pradesh"), 
	("Assam", "Assam"), 
	("Bihar", "Bihar"), 
	("Chandigarh", "Chandigarh"), 
	("Chhattisgarh", "Chhattisgarh"), 
	("Dadra Nagar Haveli", "Dadra Nagar Haveli"), 
	("Daman Diu", "Daman Diu"), 
	("Delhi", "Delhi"), 
	("Goa", "Goa"), 
	("Gujarat", "Gujarat"), 
	("Haryana", "Haryana"), 
	("Himachal Pradesh", "Himachal Pradesh"), 
	("Jammu Kashmir", "Jammu Kashmir"), 
	("Jharkhand", "Jharkhand"), 
	("Karnataka", "Karnataka"), 
	("Kerala", "Kerala"), 
	("Ladakh", "Ladakh"), 
	("Lakshadweep", "Lakshadweep"), 
	("Madhya Pradesh", "Madhya Pradesh"), 
	("Maharashtra", "Maharashtra"), 
	("Manipur", "Manipur"), 
	("Meghalaya", "Meghalaya"), 
	("Mizoram", "Mizoram"), 
	("Nagaland", "Nagaland"), 
	("Odisha", "Odisha"), 
	("Puducherry", "Puducherry"), 
	("Punjab", "Punjab"), 
	("Rajasthan", "Rajasthan"), 
	("Sikkim", "Sikkim"), 
	("Tamil Nadu", "Tamil Nadu"), 
	("Telangana", "Telangana"), 
	("Tripura", "Tripura"), 
	("Uttar Pradesh", "Uttar Pradesh"), 
	("Uttarakhand", "Uttarakhand"), 
	("West Bengal", "West Bengal"), 
]

FACILITY_CHOICES = [("YES", "Yes"), ("NO", "No"), ]

class VaccineUpdateForm(forms.ModelForm):
	name = forms.CharField(max_length=150, 
							widget=forms.TextInput(attrs={"class": "form-control"}))
	age = forms.CharField(widget=forms.NumberInput(attrs={"class": "form-control", 
															"max": 100, 
															"min": 1, }))
	state = forms.CharField(max_length=100, 
							widget=forms.Select(choices=STATE_CHOICES,
								attrs={"class": "custom-select state",
										"data-style": "btn-success",}))
	district = forms.CharField(max_length=100, 
							widget=forms.Select(choices=DISTRICT_CHOICES,
								attrs={"class": "custom-select district"}))
	city = forms.CharField(max_length=100, required=False,
							widget=forms.TextInput(
								attrs={"class": "form-control", }, ), )
	

	email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}), required=False,)
	mobile_number = forms.CharField(
							widget=forms.NumberInput(attrs={"class": "form-control", 
															"max": 9999999999, 
															"onKeyPress": "if(this.value.length==10) return false;"}))

	class Meta:
		model = VaccineUpdate
		fields = [
			"name",
			"age",
			"state",
			"district",
			"email",
			"mobile_number",
		]


class HospitalRegisterForm(forms.ModelForm):
	name = forms.CharField(max_length=150, 
							widget=forms.TextInput(
								attrs={"class": "form-control validate", }, ), )
	mobile_number = forms.CharField(
							widget=forms.NumberInput(
								attrs={"class": "form-control", 
								"onKeyPress": "if(this.value.length==10) return false;"}, ), )
	email = forms.CharField(max_length=100, required=False,
							widget=forms.EmailInput(
								attrs={"class": "form-control", }, ), )

	state = forms.CharField(max_length=100, 
							widget=forms.Select(choices=STATE_CHOICES,
								attrs={"class": "custom-select state", }, ), )
	district = forms.CharField(max_length=100, 
							widget=forms.Select(choices=DISTRICT_CHOICES,
								attrs={"class": "custom-select district", }, ), )
	city = forms.CharField(max_length=100, required=False,
							widget=forms.TextInput(
								attrs={"class": "form-control", }, ), )

	hospital_name = forms.CharField(max_length=250, 
							widget=forms.TextInput(
								attrs={"class": "form-control", }, ), )
	number_of_beds = forms.CharField(
							widget=forms.NumberInput(
								attrs={"class": "form-control", 
								"onKeyPress": "if(this.value.length==5) return false;"}, ), )

	hospital_contact_number = forms.CharField(
							widget=forms.NumberInput(
								attrs={"class": "form-control", 
								"onKeyPress": "if(this.value.length==10) return false;"}, ), )
	hospital_email = forms.CharField(required=False,
							widget=forms.EmailInput(
								attrs={"class": "form-control", }, ), )

	insurance_facility = forms.CharField(max_length=3, 
							widget=forms.Select(choices=FACILITY_CHOICES,
								attrs={"class": "custom-select", }, ), )
	ventilator_facility = forms.CharField(max_length=3, 
							widget=forms.Select(choices=FACILITY_CHOICES,
								attrs={"class": "custom-select", }, ), )

	address = forms.CharField(max_length=500, 
							widget=forms.Textarea(
								attrs={"class": "md-textarea form-control", 
										"rows": "3"}, ), )
	hospital_website = forms.CharField(max_length=500, required=False,
							widget=forms.URLInput(
								attrs={"class": "form-control", }, ), )

	class Meta:
		model = HospitalRegister
		fields = [
			"name", 
			"mobile_number", 
			"email", 
			"state", 
			"district", 
			"city",
			"hospital_name", 
			"number_of_beds", 
			"hospital_contact_number", 
			"hospital_email", 
			"insurance_facility", 
			"ventilator_facility", 
			"address", 
			"hospital_website", 
		]