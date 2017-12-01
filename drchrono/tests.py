from django.test import TestCase
from models import *
# Create your tests here.

a = {u'status': u'No Show', u'icd9_codes': [], u'office': 208234, u'base_recurring_appointment': 51487256, u'color': u'#4e9a06', u'updated_at': u'2017-11-19T22:11:36', u'last_billed_date': u'2017-11-18T09:00:00', u'deleted_flag': False, u'primary_insurer_payer_id': u'', u'duration': 45, u'id': u'69403988', u'scheduled_time': u'2017-11-18T09:00:00', u'secondary_insurer_name': u'', u'doctor': 199480, u'primary_insurance_id_number': u'', u'is_walk_in': False, u'billing_provider': None, u'profile': None, u'patient': 69742112, u'cloned_from': None, u'exam_room': 1, u'first_billed_date': u'2017-11-18T09:00:00', u'reason': u'General Visit', u'secondary_insurer_payer_id': u'', u'recurring_appointment': True, u'secondary_insurance_id_number': u'', u'primary_insurer_name': u'', u'notes': u'', u'icd10_codes': [], u'billing_status': u'No Show', u'created_at': u'2017-11-10T18:25:02'}

new_appointment = Appointment(appointment_id=str(appointment_id),
                                              duration=a.get('duration'),
                                              doctor_id=str(a.get('doctor')),
                                              scheduled_time=scheduled_time,
                                              patient_id=patient_id,
                                              patient_SSN=patient_info['social_security_number'],
                                              patient_first_name=patient_info['first_name'],
                                              patient_last_name=patient_info['last_name']
                                              )

print Appointment.objects.filter(patient_first_name=u'Arielle',
                                     patient_last_name=u'Mandelberg',
                                     scheduled_time__day=18,
                                     scheduled_time__month=11,
                                     scheduled_time__year=2017)