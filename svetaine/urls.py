
from django.contrib import admin
from django.urls import path, include

from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('',views.indexView,name="home"),
    path('klausimo_ivedimas/', views.klausimoIvedimoVaizdas, name='klausimo_ivedimo'),

]
