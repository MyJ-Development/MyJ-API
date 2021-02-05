"""bundle_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from .auth.views import AuthView
from .user.views import UserView, UserSettings

from .scheduler.views import  SchedulerTechOrderView,SchedulerTrackingView,SchedulerUserView,SchedulerMedioDePagoView,SchedulerPrioridadView,SchedulerTicketStatusView ,SchedulerClientStatusView ,SchedulerClientView,SchedulerResidenceView,SchedulerTechnicianView,SchedulerOrderView,SchedulerOrderTypeView,OrderByClientView
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='API MyJ')

urlpatterns = [
    url('docs', schema_view),
    url('scheduler/clientstatus', SchedulerClientStatusView.as_view(), name='ClientStatus'),
    url('scheduler/techtypeorder', SchedulerTechOrderView.as_view(), name='TechOrderType'),
    url('scheduler/ticketstatus', SchedulerTicketStatusView.as_view(), name='TicketStatus'),
    url('scheduler/mediodepago', SchedulerMedioDePagoView.as_view(), name='mediodepago'),
    url('scheduler/users', SchedulerUserView.as_view(), name='Users'),
    url('scheduler/seguimientos', SchedulerTrackingView.as_view(), name='Seguimientos'),
    url('scheduler/prioridad', SchedulerPrioridadView.as_view(), name='Prioridad'),
    url('scheduler/client', SchedulerClientView.as_view(), name='Clients'),
    url('scheduler/residence', SchedulerResidenceView.as_view(), name='Residences'),
    url('scheduler/technician', SchedulerTechnicianView.as_view(), name='Technicians'),
    url('scheduler/order', SchedulerOrderView.as_view(), name='Orders'),
    url('scheduler/typeorder', SchedulerOrderTypeView.as_view(), name='OrderTypes'),
    url('scheduler/cl-orders', OrderByClientView.as_view(), name='OrderByClient'),
    url('users/current', UserView.as_view(), name='Current user'),
    url('auth/login', AuthView.login, name='User login'),
    url('auth/sign-up', AuthView.sign_up, name='Sign up a new user'),
    url('auth/request-pass', AuthView.request_pass, name='Send an email with password'),
    url('auth/reset-pass', AuthView.reset_pass, name='Reset a pasword'),
    url('auth/sign-out', AuthView.sign_out, name='Sign out'),
    url('auth/refresh-token', AuthView.refresh_token, name='Refresh a token'),
    url('settings/current', UserSettings.as_view(), name='User settings'),
]
