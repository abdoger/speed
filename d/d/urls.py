"""
URL configuration for mtcoffee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib import admin
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from django.urls import path,include
from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf.urls.i18n import i18n_patterns
from .sitemaps import StaticViewSitemap,ProductViewSitemap
from django.contrib.sitemaps.views import sitemap
sitemaps ={'static':StaticViewSitemap,'products':ProductViewSitemap}
from .views import *
urlpatterns = [
    path('il8n/', include('django.conf.urls.i18n')),
]
urlpatterns += i18n_patterns(
    path('api-auth/', include('rest_framework.urls')),
    # path('admin/', include('admin_honeypot.urls', )),
    path('sitemaps.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.django.contrib.sitemap'),
    path('robots.txt',TemplateView.as_view(template_name='robots.txt',content_type='text/plain')),

    path('social-auth/' , include('social_django.urls', namespace='social')),
    path('accounts/',include('accounts.urls')),
    path('secret/', admin.site.urls),
    path('',  include('product.urls')),
    path('pages/',  include('pages.urls')),

   
    path('orders/', include('orders.urls')),
    path ('h',home_view,name='home-view'),
    path ('login/',auth_view,name='login-view'),

    path ('verify/',verify_view,name='verify-view'),

  
)
urlpatterns  += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handel404 = 'mtcoffee.views.handel404'
handel405 = 'mtcoffee.views.handel405'




