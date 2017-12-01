# Create your views here.
from django.http import Http404

from constants import (
    statistic_averaged_appointment_perday,
    statistic_averaged_waiting_time
)

from django.http import HttpResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
import logging
from forms import (
    PatientForm,
    DemographicForm
)
from models import *
import json


logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('Django-view')
logger.setLevel(logging.INFO)

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'index.html', {})


@login_required
@transaction.atomic
def login_redirect(request):
    """
    Redirect page for doctor login
    Update the database with the current access token
    If the user does not exist, create the corresponding object
    """
    user = request.user
    try:
        extra_data = user.social_auth.get(provider='drchrono').extra_data
        # current_doctor = Doctor.api_request_drchrono(extra_data.get('access_token'), 'api/users/current', 'GET')
        current_doctor = Doctor.get_doctor_info(extra_data.get('access_token'))
    except ObjectDoesNotExist:
        return HttpResponse('Authentication error')
    except Exception as e:
        return HttpResponse('Failed to get user information through API')

    user_info = {
        'doctor_name': current_doctor.get('username'),
        'access_token': extra_data.get('access_token'),
        'refresh_token': extra_data.get('refresh_token'),
        'time_out': extra_data.get('expires_in'),
        'token_type': extra_data.get('token_type'),
    }
    logger.info("user_info is %s" % user_info)

    user_data = dict(current_doctor)
    print request.user
    # If the doctor is not in the database
    doctor = Doctor.objects.filter(user_id=user_data['doctor'])
    if not doctor:
        Doctor(
            user_id=user_data['doctor'],
            user=user_data['username'],
            access_token=user_info['access_token']
        ).save()
    else:
        d = Doctor.objects.get(user_id=user_data['doctor'])
        d.access_token = extra_data.get('access_token')
        d.save()

    return render(request, "login_success.html", {'doctor': user_info})


@login_required
@transaction.atomic
def kiosk_dashboard(request):
    """
    Kiosk dashboard page for doctor, include the data analytic part(waiting time, appointments count,
    today's appointment progress).
    """
    try:
        access_token = request.user.social_auth.get(provider='drchrono').extra_data.get('access_token')
        logger.info('access token is %s' % access_token)
        doctor = Doctor.objects.get(access_token=access_token)
    except ObjectDoesNotExist:
        return HttpResponse('Authentication Failed')
    except Exception as e:
        logger.debug("Unidentified error in handling dashboard view")
        return HttpResponse('An error has occured')

    # Todo All time field should be changed from seconds to minutes for representation
    # Todo Add the recent time
    avg_waiting_time = doctor.update_average_waiting_time() / 60
    # just changed to timezone.now
    logger.info("today is %s" % str(timezone.now().date()))
    apps = Doctor.get_schedule(access_token, str(datetime.datetime.now().date()))
    #historical apps data stored in db
    historical_apps = Appointment.objects.filter(doctor_id=doctor.user_id).order_by('-scheduled_time')

    # logger.info("type of apps is %s" % type(historical_apps))
    # logger.info("historical_apps %s" % historical_apps)

    # Figure out how much app has been done today
    print apps
    complete_counter = 0
    for app in apps:
        if app['status'] == 'Complete':
            complete_counter += 1
        else:
            print app['status']

    # progress bar
    complete_percentage = 0
    try:
        complete_percentage = 100 * complete_counter / float(len(apps))
    except ZeroDivisionError:
        logger.info('No appointment for date %s' % datetime.datetime.now().date())

    # Todo support upcoming appointments
    # count the appointments/day
    upcoming_app_counter = 5
    upcoming_app_list = []

    unique_dates_set = set()
    for app in historical_apps:
        unique_dates_set.add(app.scheduled_time.date())
        now = timezone.now()
        if app.scheduled_time > now:
            upcoming_app_list.append(app)

    # logger.info("upcoming app list is %s" % upcoming_app_list)

    app_perday = len(historical_apps) / len(unique_dates_set)
    user_data = {'username': request.user, 'patients': Doctor.get_patient_list(access_token),
                 'appointments': apps,
                 'doctor': doctor,
                 'average_waiting_time': "%.1f" % round(avg_waiting_time),
                 'waiting_time_larger': avg_waiting_time >= statistic_averaged_waiting_time,
                 'appointments_per_day': app_perday,
                 'compared_waiting_time': "%.1f" % round(abs(avg_waiting_time - statistic_averaged_waiting_time),2),
                 'appointment_number_larger': app_perday - statistic_averaged_appointment_perday >= 0,
                 'compared_appointment_per_day': abs(app_perday - statistic_averaged_appointment_perday),
                 'finished_percentage': "%.1f" % round(complete_percentage),
                 'upcoming_app_list': upcoming_app_list
                 }
    # logger.info('user data is %s' % user_data)

    return render(request, "dashboard.html", user_data)


@login_required
@transaction.atomic
def kiosk_schedule(request):
    # Todo handle the case the user jump to schedule url instead of login redirect
    """
    Schedule page for the drchrono kiosk
    """
    #Todo support auto email notification
    access_token = request.user.social_auth.get(provider='drchrono').extra_data.get('access_token')
    # Todo map the patient id to patient name
    # Todo All time field should be changed from seconds to minutes for representation
    patient_dictionary = {}
    for p in Doctor.get_patient_list(access_token):
        patient_dictionary[p['id']] = p['first_name'], p['last_name']

    apps = Doctor.get_schedule(access_token, str(datetime.datetime.now().date()))
    for a in apps:
        a['patient_first_name'], a['patient_last_name'] = patient_dictionary.get(a['patient'])
        print a

    user_data = {'username': request.user,
                 'appointments': apps
                 }
    return render(request, "schedule.html", user_data)


@login_required
def kiosk_patients(request):
    # Todo handle the case the user jump to schedule url instead of login redirect?
    """
    Patient list page for drchrono kiosk, support bew appointment arragement
    """
    # Todo support new appointment arragement
    try:
        access_token = request.user.social_auth.get(provider='drchrono').extra_data.get('access_token')
        user_data = {'username': request.user, 'patients': Doctor.get_patient_list(access_token)
                    }
    except Exception as e:
        raise Http404
    # print user_data
    return render(request, "kiosk_patients.html", user_data)


@login_required
def doctor_checkin_patient(request, app_id):
    """
    check in the patient for given appointment
    """
    access_token = request.user.social_auth.get(provider='drchrono').extra_data.get('access_token')
    context = {
        'operation_success': Doctor.check_in_patient(access_token, {'id':  app_id})
    }

    posts = json.dumps(context)
    print "operation_success is  %s" % context['operation_success']
    return HttpResponse(posts, content_type="application/json")


@login_required
def doctor_finish_appointment(request, app_id):
    """
    Finish the appointment with the patient for the given appointment
    """
    access_token = request.user.social_auth.get(provider='drchrono').extra_data.get('access_token')
    try:
        context = {
            'operation_success': Doctor.finish_appointment(access_token, {'id':  app_id})
        }
    except Exception as e:
        raise Http404
    posts = json.dumps(context)
    print context['operation_success']
    return HttpResponse(posts, content_type="application/json")


@login_required
def send_email(request, patient_id):
    """
    Send the email given the recipient_list and content
    :return: operation result
    """
    # Todo catch the error
    user = request.user
    email_body = """
    An email body
    """
    send_mail(subject="Appointments Reminder",
              message=email_body,
              from_email="emailtestyao@gmail.com",
              recipient_list=["Ly417743771@gmail.com"])
    return render(request, "index.html")


def test_refresh(request):
    """
    :param request:
    :return:
    """
    data = Doctor.request_new_token('jzd2bGrikUW1J4szWzIQi9NXIq1rb5')
    print data
    current_doctor = Doctor.api_request_drchrono(data.get('access_token'), 'api/users/current', 'GET')
    doctor = Doctor.objects.get(user_id=current_doctor.get('doctor'))
    doctor.access_token = data.get('access_token')
    doctor.save()
    return render(request, "index.html")


def patient_self_checkin(request):
    """
    Patient self check-in page
    """
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")

            appointments = Appointment.objects.filter(patient_first_name=first_name,
                                                      patient_last_name=last_name).order_by('scheduled_time')

            doctors = {}
            # return only the pending appointments today, appointments overwritten here
            appointments = [app for app in appointments if app.scheduled_time.date()
                            >= datetime.datetime.now().date()]
            for a in appointments:
                doctors[a.doctor_id] = a.get_doctor_name()

            doctor_list = [doctors[a.doctor_id] for a in appointments]
            reformatted_app_time = []
            status_list = []
            can_checkin = []
            for a in appointments:
                # e.g. 14:50:00
                splited_time = str(a.scheduled_time).split()[-1].split('+')[0]
                print "splited", splited_time
                reformatted_app_time.append(splited_time)
                # Todo consider to change the schema for appointment
                access_token = Doctor.objects.get(user_id=a.doctor_id).access_token
                status = Doctor.get_appointment_status(access_token, a.appointment_id)
                status_list.append(status)
                logger.info('status received as %s' % status)
                not_check_in_status = ['Checked In', 'Arrived', 'In Room', 'Cancelled', 'In Session', 'No Show', 'Not Confirmed', 'Rescheduled', 'Complete']
                if status in not_check_in_status:
                    can_checkin.append(False)
                else:
                    can_checkin.append(True)

            app_doctor_list = zip(appointments, doctor_list, reformatted_app_time, status_list, can_checkin)
            context = {
                'app_doctor': app_doctor_list,
                'patient_first_name': first_name,
                'patient_last_name': last_name,
            }
            print app_doctor_list
            # print Doctor.get_patient_demograph('MY4CCJGbVW3Rq88fdQMzWmG23zIYah', 'Jenny', 'Harris')
            return render(request, "patient_appointments.html", context)
        else:
            context = {
                'form': form
            }
            return render(request, "patient_check_in.html", context)
    else:
        context = {'form': PatientForm}
        return render(request, "patient_check_in.html", context)


@csrf_protect
@transaction.atomic
def demographic_form_filler(request, app_id):
    """
    Found the appointment, fill the demographic
    """
    if request.method == 'POST':
        logger.info('appid is %s' % app_id)
        form = DemographicForm(request.POST)
        if form.is_valid():
            raw_form_data = form.cleaned_data
            form_data = {}
            for key, value in raw_form_data.iteritems():
                if value:
                    form_data[key] = value
            # Todo change the hardcoded doctor id, must provide doctor id and gender in form
            # form_data['doctor'] = 199480
            print "form_data is %s" % form_data
            appointment = Appointment.objects.get(appointment_id=app_id)
            form_data['doctor'] = appointment.doctor_id
            access_token = Doctor.objects.get(user_id=appointment.doctor_id).access_token
            if access_token:
                patch = {"status": "Arrived",
                         'id': app_id
                         }
                update_status = Doctor.update_appointment_status(access_token, patch)
                update_demograph = Doctor.update_patient_demograph(access_token, appointment.patient_id, form_data)

                context = {
                    'operation_success': update_status,
                    'update_demograph_success': update_demograph,
                    'app_id': app_id
                }
                # save the arrived time for patient
                try:
                    app = Appointment.objects.get(appointment_id=app_id)
                    app.arrived_time = timezone.now()
                    app.save()
                except ObjectDoesNotExist:
                    messages.error(request, "Failed to find the appointment in database")
                except Exception:
                    messages.error(request, "Unidentified error")

                print "Your arrived time is %s" % get_object_or_404(Appointment, appointment_id=app_id).arrived_time
                return render(request, "patient_check_in_status.html", context)
            else:
                # didn't find the access token this should not happen
                messages.error(request, "Failed to access the appointment")
                return render(request, "patient_check_in.html")

    else:
        try:
            a = Appointment.objects.get(appointment_id=app_id)
        except ObjectDoesNotExist:
            messages.error(request, "The appointment does not exist!")
            return render(request, "patient_check_in.html", {})
        except Exception as e:
            messages.error(request, "Unknown error in getting appointment!")

        if a.arrived_time:
            messages.error(request, "You have alreday checked in for this appointment, redirected to login page")
            return render(request, "patient_check_in.html", {'form': PatientForm})

        context = {'form': DemographicForm,
                   'app_id': app_id,
                   }
        return render(request, "patient_demograph.html", context)


@login_required
def gg(request):
    """
    Test page
    """
    import datetime
    from django.core.urlresolvers import reverse
    from django.http import HttpResponseRedirect
    import requests
    import time
    from django.utils.dateparse import parse_datetime
    from smtplib import SMTP
    from email.mime.text import MIMEText
    logger.info('Doing test')
    access_token = Doctor.objects.get(user_id=199480).access_token
    m = Doctor.api_request_drchrono(access_token, "api/appointments/%s" % 71440822, 'GET')
    print 'status is', dict(m)['status']
    endpoint = '/api/appointments'
    # #Doctor.check_in_patient(access_token, {'id': 69403880})
    # Doctor.update_appointment_status(access_token, {'id': u'69403916', 'status': 'Arrived'})
    # Doctor.update_patient_demograph(access_token, 69742112, {'doctor': 199480,
    #                                 'gender': u'Male',}
    #                                 )
    # print access_token

    # if access_token:
    #     patch = {"status": "Arrived",
    #              'id': 69403968
    #              }
    #     update_status = Doctor.update_appointment_status(access_token, patch)
    # context = {}
    # app = get_object_or_404(Appointment, appointment_id=111111)
    # try:
    #     a = Appointment.objects.get(appointment_id=122222)
    # except ObjectDoesNotExist:
    #     messages.error(request, "The appointment does not exist!")
    # apps = Appointment.objects.filter(doctor_id=199480)
    # for a in apps:
    #     print "scheduled time is %s" % a.scheduled_time
    #     print "waiting time is {0}, arrived time is {1}".format(a.waiting_time, a.arrived_time)
    return render(request, "gg.html", {})

