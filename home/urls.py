from django.contrib.sitemaps.views import sitemap
from django.urls import path
from .views import (home_view, 
					district_view, 
					vaccine_update_view, 
					hospital_register_view, 
					verified_hospital_view, sitemap_view, privacy_policy_view, )

urlpatterns = [
    path("", home_view, name="home_view"),
    path("vaccine-update/", vaccine_update_view, name="vaccine_update_view"),
    path("hospital-register/", hospital_register_view, name="hospital_register_view"),
    path("verified-hospital/", verified_hospital_view, name="verified_hospital_view"),
    path("sitemap.xml", sitemap_view, name="sitemap_view"),
    path("privacy-policy", privacy_policy_view, name="privacy_policy_view"),
    path("<str:state>/", district_view, name="district_view"),
]
