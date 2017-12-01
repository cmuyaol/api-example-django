from django.conf.urls import (
    include,
    url
)
from django.views.generic import TemplateView
import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^login_redirect', views.login_redirect),
    url(r'test_refresh', views.test_refresh),
    url(r'^kiosk/schedule', views.kiosk_schedule, name='kiosk_schedule'),
    url(r'^kiosk/patients', views.kiosk_patients, name='kiosk_patients'),
    url(r'^kiosk', views.kiosk_dashboard, name='kiosk_dashboard'),
    url(r'^doctor_checkin_patient/(?P<app_id>\d+)', views.doctor_checkin_patient, name='doctor_checkin_patient'),
    url(r'^doctor_finish_appointment/(?P<app_id>\d+)', views.doctor_finish_appointment, name='doctor_finish_appointment'),
    url(r'^patient_checkin', views.patient_self_checkin, name='patient_checkin'),
    url(r'^update_demograph/(?P<app_id>\d+)', views.demographic_form_filler, name='update_demograph'),
    url(r'^send_email/(?P<patient_id>\d+)', views.send_email, name='send_email'),
    url(r'user_logout', views.logout_view, name='kiosk_logout'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^gg$', views.gg, name="gg"),
]
