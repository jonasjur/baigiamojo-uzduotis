from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('',views.indexView,name="home"),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('login/',LoginView.as_view(),name="login_url"),
    path('register/',views.registerView,name="register_url"),
    path('logout/',LogoutView.as_view(next_page='dashboard'),name="logout"),
    path('klausimo_ivedimas/', views.klausimoIvedimoVaizdas, name='klausimo_ivedimo'),
    path('klausimai/<int:klausimo_id>/', views.atvaizduotiKlausima, name='klausimo_atvaizdavimas'),
    path('like_answer/<int:answer_id>/', views.like_answer, name='like_answer'),

]