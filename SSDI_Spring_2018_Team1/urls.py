"""SSDI_Spring_2018_Team1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     url(r'^index/', TemplateView.as_view(template_name="index.html")),
# ]


from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from beton.views import Dbtest
from beton.views import post_collection

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', TemplateView.as_view(template_name="index.html")),
    url(r'^dbtest/', Dbtest),
    url(r'^api/v1/user/$', post_collection, name='post_collection'),

]

