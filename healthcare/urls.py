from django.urls import path
from . import views

urlpatterns = [
    # guest urls
    path('', views.home, name='home'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout_user'),
    path('contact/', views.contact, name = 'contact'),
    path('about/', views.about, name = 'about'),
    path('guestAddPatient/<int:pk>/', views.guestAddPatient, name = 'guestAddPatient'),
    path('guestRegister_patient/', views.guestRegister_patient, name = 'guestRegister_patient'),
    # admin urls
    path('index/', views.index, name = 'index'),
    path('register/', views.register_user, name = 'register'),
    path('register_doc/', views.register_doc, name = 'register_doc'),
    path('appointment/', views.appointment, name = 'appointment'),
    path('addAppointment/', views.addAppointment, name = 'addAppointment'),
    path('deleteAppointment/<int:pk>/', views.deleteAppointment, name = 'deleteAppointment'),
    path('viewAppointment/', views.viewAppointment, name = 'viewAppointment'),
    path('addPatient_pk/<int:pk>/', views.addPatient_pk, name = 'addPatient_pk'),
    path('addPatient/', views.addPatient, name = 'addPatient'),
    path('patientsList/', views.patientsList, name = 'patientsList'),
    path('patient/<int:pk>/', views.patient, name = 'patient'),
    path('deletePatient/<int:pk>/', views.deletePatient, name = 'deletePatient'),
    path('addDoctor/', views.addDoctor, name = 'addDoctor'),
    path('addDoctor_pk/<int:pk>/', views.addDoctor_pk, name = 'addDoctor_pk'),
    path('doctor/<int:pk>/', views.doctor, name = 'doctor'),
    path('deleteDoctor/<int:pk>/', views.deleteDoctor, name = 'deleteDoctor'),
    path('viewDoctor/', views.viewDoctor, name = 'viewDoctor'),
    # doctor urls
    path('doctorHome/', views.doctorHome, name = 'doctorHome'),
    path('doctor_view_patient/<int:pk>/', views.doctor_view_patient, name = 'doctor_view_patient'),
    path('doctor_deleteAppointment/<int:pk>/', views.doctor_deleteAppointment, name = 'doctor_deleteAppointment'),
    path('doctor_editAppointment/<int:pk>/', views.doctor_editAppointment, name = 'doctor_editAppointment'),
    path('doctor_add_appointment', views.doctor_add_appointment, name = 'doctor_add_appointment'),
    # patient urls 
    path('patientHome/', views.patientHome, name = 'patientHome'),
    path('patientViewAllDoctors/', views.patientViewAllDoctors, name = 'patientViewAllDoctors'),
    path('patientAddAppointments/', views.patientAddAppointments, name = 'patientAddAppointments'),
    path('patient_view_doctor/<int:pk>/', views.patient_view_doctor, name = 'patient_view_doctor'),
    path('tables/', views.tables, name = 'tables'),
]

