from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# Create your models here.

mobile_regex = RegexValidator(regex=r"^\d{10}$", 
									message="Mobile Number Enter in 10 Digit Formate")
FACILITY_CHOICES = [("YES", "Yes"), ("NO", "No"), ]

class VaccineUpdatePost(models.Model):
	title = models.CharField(max_length=500, )
	link = models.URLField(max_length=700, )
	source = models.CharField(max_length=250, )
	description = models.TextField(null=True, blank=True, )
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.title}"

class VaccineUpdate(models.Model):
	""" Vaccine Update Model for Vaccine Update List """

	name = models.CharField(max_length=150, )
	age = models.IntegerField(validators=[
											MinValueValidator(limit_value=1,
											message="Must be Greater than Zero"),
											MaxValueValidator(limit_value=100,
											message="Must be less than or Equal to 100")
											])

	state = models.CharField(max_length=100, )
	district = models.CharField(max_length=100, )
	city = models.CharField(max_length=100, null=True, blank=True, )

	email = models.EmailField(null=True, blank=True, )
	mobile_number = models.CharField(max_length=10, validators=[mobile_regex, ])

	def __str__(self):
		return f"{self.name} - {self.email} - {self.mobile_number}"


class HospitalRegister(models.Model):
	verified = models.BooleanField(default=False, )

	name = models.CharField(max_length=150, )
	mobile_number = models.CharField(max_length=10, validators=[mobile_regex, ])
	email = models.EmailField(null=True, blank=True, )

	state = models.CharField(max_length=100, )
	district = models.CharField(max_length=100, )
	city = models.CharField(max_length=100, null=True, blank=True, )

	hospital_name = models.CharField(max_length=250, )
	number_of_beds = models.IntegerField(validators=[
											MinValueValidator(limit_value=1,
											message="Must be Greater than Zero"), ])
	hospital_contact_number = models.CharField(max_length=10, validators=[mobile_regex, ])
	hospital_email = models.EmailField(null=True, blank=True, )


	insurance_facility = models.CharField(max_length=3, 
											choices=FACILITY_CHOICES, 
											default="YES", )
	ventilator_facility = models.CharField(max_length=3, 
											choices=FACILITY_CHOICES, 
											default="YES", )

	address = models.TextField(max_length=500, )
	hospital_website = models.URLField(max_length=500, null=True, blank=True, )

	def __str__(self):
		return f"""{self.hospital_name} - {self.number_of_beds} - 
					{self.hospital_contact_number} - {self.hospital_email}"""