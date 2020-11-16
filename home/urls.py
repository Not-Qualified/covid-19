from django.urls import path
from django.views.generic import TemplateView
from .views import (home_view, 
					district_view, vaccine_update_view, hospital_register_view, 
					verified_hospital_view, chart_view, contact_us_view)

urlpatterns = [
    path("chart/", chart_view, name="chart_view"),
    path("", home_view, name="home_view"),
    path("abc/", home_view, ),
    path("vaccine-update/", vaccine_update_view, name="vaccine_update_view"),
    path("hospital-register/", hospital_register_view, name="hospital_register_view"),
    path("verified-hospital/", verified_hospital_view, name="verified_hospital_view"),
    path("contact-us/", contact_us_view, name="contact_us_view"),
    path("testing-center/", TemplateView.as_view(template_name="home/testing-center.html"), name="testing_center_view"),
    path("privacy-policy/", TemplateView.as_view(template_name="privacy-policy.html"), name="privacy_policy_view"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("sitemap.xml", 
        TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml"), 
        name="sitemap_view"),
    path("robots.txt/", 
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), 
        name="robots.txt"),
    path("ads.txt/", 
        TemplateView.as_view(template_name="ads.txt", content_type="text/plain"), 
        name="ads.txt"),
    path("googled9bb73c359cc1dce.html",
        TemplateView.as_view(template_name="googled9bb73c359cc1dce.html", content_type="text/html"), 
        name="google-html", ),
    path("<str:state>/", district_view, name="district_view"),
]
