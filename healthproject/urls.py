from django.conf.urls import patterns,include, url
from django.contrib import admin
from rest_framework import routers
from healthprojectapp import views

admin.autodiscover()

router=routers.DefaultRouter()
router.register(r'health',views.HealthViewSet)

urlpatterns = patterns('',
    # Examples:
     url(r'^', include(router.urls)),
     url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),

     url(r'^admin/', include(admin.site.urls)),
	url(r'^login/','healthprojectapp.views.login'),
	url(r'^auth/','healthprojectapp.views.auth_view'),
	url(r'^home/','healthprojectapp.views.home'),
	url(r'^logindetails/','healthprojectapp.views.logindetails'),
	url(r'^login/','healthprojectapp.views.login'),
	url(r'^logout/','healthprojectapp.views.logout'),
	url(r'^pdetails/','healthprojectapp.views.pdetails'),
	#load all details in different page
	url(r'^formsubmit/','healthprojectapp.views.formsubmit'),
	url(r'^archive/','healthprojectapp.views.archive'),
)
