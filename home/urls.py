from django.urls import path
from django.views.generic import TemplateView
from .views import (home_view, 
					district_view, vaccine_update_view, hospital_register_view, 
					verified_hospital_view, )

urlpatterns = [
    path("", home_view, name="home_view"),
    path("vaccine-update/", vaccine_update_view, name="vaccine_update_view"),
    path("hospital-register/", hospital_register_view, name="hospital_register_view"),
    path("verified-hospital/", verified_hospital_view, name="verified_hospital_view"),
    path("privacy-policy/", TemplateView.as_view(template_name="privacy-policy.html"), name="privacy_policy_view"),
    path("contact-us/", TemplateView.as_view(template_name="contact-us.html"), name="contact_us_view"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("sitemap.xml", 
        TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml"), 
        name="sitemap_view"),
    path("robots.txt/", 
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), 
        name="robots.txt"),
    path("googled9bb73c359cc1dce.html",
        TemplateView.as_view(template_name="googled9bb73c359cc1dce.html", content_type="text/html"), 
        name="google-html", ),
    path("<str:state>/", district_view, name="district_view"),
]
