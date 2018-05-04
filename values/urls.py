from django.conf.urls import url

from . import views

urlpatterns = [
	url('^(?P<name>[a-zA-Z]+)/get_user/$',views.get_user,name='user'),
	url('^$',views.index, name='index'),
	url('^data/$',views.data,name='data'),
	url('^login/$',views.login,name='login'),
	url('^logout/$',views.logout,name="logout"),
	url('^register/$',views.register,name='register'),
	url('^add_register/$',views.add_register,name='add_register'),
	url('^check_login/$',views.check_login,name='check_login'),
	url('^check_login/+(?P<uid>[a-zA-Z]+)/give_toll/$',views.give_toll,name='toll'),
	url('^check_login/+(?P<uid>[a-zA-Z]+)/tollbooth_values/$',views.tollbooth_values,name='tollbooth'),
	url('^check_login/+(?P<pid>[a-zA-Z]+)/tollbooth_payments/$',views.tollbooth_payments,name='tollboothpay'),
	url('^check_login/check_login/+(?P<uid>[a-zA-Z]+)/tollbooth_values/$',views.tollbooth_values,name='tollbooth'),
	url('^check_login/check_login/+(?P<pid>[a-zA-Z]+)/tollbooth_payments/$',views.tollbooth_payments,name='tollboothpay'),
	url('^check_login/chart',views.chart,name="chart")
	#url('^make/$',views.make,name="fruits")
]
