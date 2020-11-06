from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

from PIL import Image

# Create your models here.

mobile_regex = RegexValidator(regex=r"^\d{10}$", 
									message="Mobile Number Enter in 10 Digit Formate")

landline_regex = RegexValidator(regex=r"^\d{12}$", 
									message="LandLine Number Enter in 12 Digit Formate - If It's less than 12 Digit try with leading number as 0 and make it 12")

FACILITY_CHOICES = [("YES", "Yes"), ("NO", "No"), ]

class VaccineUpdatePost(models.Model):
	title = models.CharField(max_length=500, )
	link = models.URLField(max_length=700, )
	source = models.CharField(max_length=250, )
	image = models.ImageField(upload_to="post_images", null=True, blank=True, )
	description = models.TextField(null=True, blank=True, )
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.title}"

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.image.path)
		img.thumbnail((1024, 768), Image.ANTIALIAS)
		img.save(self.image.path)

	def delete(self, *args, **kwargs):
		storage, path = self.image.storage, self.image.path
		super().delete(*args, *kwargs)
		storage.delete(path)


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
	landline_number = models.CharField(max_length=12, validators=[landline_regex, ], null=True, blank=True, )

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
	hospital_landline = models.CharField(max_length=12, validators=[landline_regex, ], null=True, blank=True, )
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


class ContactUsList(models.Model):
	name = models.CharField(max_length=100, )
	mobile_number = models.CharField(max_length=10, null=True, blank=True, validators=[mobile_regex, ])
	message = models.TextField(max_length=5000, )

	def __str__(self):
		return f"{self.name} - {self.mobile_number}"



class HitCounter(models.Model):
	hit_count = models.BigIntegerField(default=0, )

	def __str__(self):
		return f"Total Views : {self.hit_count}"