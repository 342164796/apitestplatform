"""apitestplatform URL Configuration

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

from django.conf.urls import url
from base.views import *

urlpatterns = [

    url(r'/project/', project_index),
    url(r'/project_add/', project_add),
    url(r'/project_update/', project_update),
    url(r'/project_delete/', project_delete),

    url(r'/sign/', sign_index),
    url(r'/sign_add/', sign_add),
    url(r'/sign_update/', sign_update),
    url(r'/sign_delete/', sign_delete),

    url(r'/env/', env_index),
    url(r'/env_add/', env_add),
    url(r'/env_update/', env_update),
    url(r'/env_delete/', env_delete),

    url(r'/interface/', interface_index),
    url(r'/interface_add/', interface_add),
    url(r'/interface_delete/', interface_delete),
    url(r'/interface_update/', interface_update),
    

    url(r'/case/', case_index),
    url(r'/case_add/', case_add),
    url(r'/case_run/', case_run),
    url(r'/case_delete/', case_delete),
    url(r'/case_update/', case_update),
    url(r'/case_search/',case_search),

    url(r'/plan/', plan_index),
    url(r'/plan_add/', plan_add),
    url(r'/plan_run/', plan_run),
    url(r'/plan_update/', plan_update),
    url(r'/plan_delete/', plan_delete),

    url(r'/report/', report_index),
    url(r'/report_detail/', report_detail),
    url(r'/findata/', findata),

    url(r'/moncfg/', moncfg),
    url(r'/mon_add/', mon_add),
    url(r'/mon_update/', mon_update),
    url(r'/mon_delete/', mon_delete),
    url(r'/monapi/', monapi),
    url(r'/monapi_add/', monapi_add),
    url(r'/monapi_delete/', monapi_delete),
    url(r'/monapi_update/', monapi_update),
    url(r'/monapi_run/', monapi_run),
    url(r'/msgcfg/', msgcfg),
    url(r'/msgcfg_update/',msgcfg_update)

]

