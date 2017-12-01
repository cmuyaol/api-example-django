from choices import *
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
import logging
import requests
from settings import (
    SOCIAL_AUTH_DRCHRONO_KEY,
    SOCIAL_AUTH_DRCHRONO_SECRET,
    URL_BASE_DRCHRONO
)

# deal with the drchrono api
# Create your models here.

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('Django-models')
logger.setLevel(logging.INFO)


class Doctor(models.Model):
    """
    Store the user information
    Handle drchrono API requests and common operations for doctors
    """
    user_id = models.IntegerField()
    user = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100, default='')
    average_waiting_time = models.IntegerField(default=5)

    @staticmethod
    def api_request_drchrono(access_token, endpoint, request_type, args={}, json_format=True):
        """
        Given the access token, API endpoint, type of the request, arguments,perform the API request.
        If json_format is set to False, return the httpResponse directly.
        This method raise for status
        :param access_token: Access_token of the user
        :param endpoint: API endpoint
        :param request_type: Type of the api request: e.g. GET, PUT, POST
        :param args: request argument
        :param json_format: If a JSON format of response is expected
        :return: api_response_drchrono: Response of the API call,
        """
        headers = {
            'Authorization': 'Bearer %s' % access_token,
        }
        api_response_drchrono = ''
        if request_type == "GET":
            api_response_drchrono = requests.get(URL_BASE_DRCHRONO + endpoint, headers=headers)
        elif request_type == "PUT":
            api_response_drchrono = requests.put(URL_BASE_DRCHRONO + endpoint, data=args, headers=headers)
        elif request_type == "POST":
            api_response_drchrono = requests.post(URL_BASE_DRCHRONO + endpoint, data=args, headers=headers)
        elif request_type == "PATCH":
            api_response_drchrono = requests.patch(URL_BASE_DRCHRONO + endpoint, data=args, headers=headers)
        else:
            raise TypeError("request type %s not supported yet" % request_type)

        api_response_drchrono.raise_for_status()
        if json_format:
            return api_response_drchrono.json()
        else:
            return api_response_drchrono

    @staticmethod
    def multiple_api_request_drchrono(self):
        pass

    @staticmethod
    def check_in_patient(access_token, appointment):
        """
        (Doctor) check in a patient for the given appointment, update the waiting time for the patient
        :param access_token: access_token of the corresponding doctor
        :param appointment: dictionary that include the appointment id
        :return:
        """
        # check if the patient is alreday checked in

        patch = {"status": "Checked In",
                 'id': appointment['id']}
        check_in_update_success = Doctor.update_appointment_status(access_token, appointment=patch)

        if check_in_update_success:
            current_time = timezone.now()
            app = Appointment.objects.get(appointment_id=appointment['id'])
            td = current_time - app.arrived_time
            # days = td.days
            hours, remainder = divmod(td.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print "waiting time previously ", app.waiting_time
            app.waiting_time = hours * 3600 + minutes * 60 + seconds
            app.save()
            print app.appointment_id
            print "waiting time is ", app.waiting_time
        else:
            print "Not success"

        return check_in_update_success

    @staticmethod
    def finish_appointment(access_token, appointment):
        """
        Update the appointment status to Complete
        :param access_token: access_token of the corresponding doctor
        :param appointment: dictionary that include the appointment id
        :return:
        """
        patch = {
            "status": "Complete",
            'id': appointment['id']
        }
        complete_app_success = Doctor.update_appointment_status(access_token, appointment=patch)
        # Todo collect time statistics
        if complete_app_success:
            pass
        else:
            pass

        return complete_app_success

    def count_finished_appointment(self):
        """
        Count the appointments the doctor has finished so far
        :return: number of the appointments finished so far
        """
        apps = Appointment.objects.filter(doctor_id=self.user_id)
        counter = 0
        for a in apps:
            if a.waiting_time is not None:
                counter += 1
        return counter

    @staticmethod
    def request_new_token(refresh_token):
        """
        Request the new access token
        :param refresh_token:
        :return: (new refresh_token, new access_token)
        """
        response = requests.post('%s%s' % (URL_BASE_DRCHRONO, 'o/token/'), data={
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
            'client_id': SOCIAL_AUTH_DRCHRONO_KEY,
            'client_secret': SOCIAL_AUTH_DRCHRONO_SECRET,
        })
        print "status code is %s" % response.status_code
        data = response.json()
        print "json data access token is %s" % dict(data)['access_token']
        return data

    @staticmethod
    def get_doctor_info(access_token):
        """
        Invoke API request to retrieve the doctor's user information
        :return:HttpResponse of JSON format
        """
        endpoint = 'api/users/current'
        return Doctor.api_request_drchrono(access_token, endpoint, 'GET')

    @staticmethod
    def get_patient(access_token, patient_id):
        """
        Invoke API request to retrieve information for a specific patient
        :param access_token: access_token of the corresponding doctor
        :param patient_id: id of the patient
        :return: Information for a specific patient
        """
        # Todo catch the exception that id and access_token does not match
        endpoint = '/api/patients/%d' % patient_id
        return Doctor.api_request_drchrono(access_token, endpoint, 'GET')

    @staticmethod
    def get_patient_list(access_token):
        """
        Invoke API request to get information of all patients of the given doctor
        :param access_token: Access_token of the user
        :return: the list of patient
        """
        patients = []
        patients_url = 'api/patients'
        while patients_url:
            data = Doctor.api_request_drchrono(access_token, patients_url, 'GET')
            patients.extend(data['results'])
            patients_url = data['next']  # A JSON null on the last page
        return patients

    @staticmethod
    def get_schedule(access_token, date_time):
        """
        Invoke API request to retreive schedule of the doctor for a given date
        :param access_token: Access_token of the user
        :param date_time: Date of format yyyy-mm-dd e.g. 2017-11-17
        :return: schedule: the appointments sorted by the datetime
        """
        # patient_list = Doctor.get_patient_list(access_token)
        appointments = []

        appointment_url = 'api/appointments?date=%s' % date_time
        while appointment_url:
            response = Doctor.api_request_drchrono(access_token, appointment_url, 'GET')
            appointments.extend(response['results'])
            appointment_url = response['next']

        # Update the appointments in the database
        print "get date time as %s" % date_time
        return Doctor.update_appointment(access_token, appointments)

    @staticmethod
    def get_patient_demograph(access_token, first_name, last_name):
        """
        Invoke API request to retrieve the patient demograph of a given doctor
        given the First name and Last name
        :param access_token: Access_token of the user
        :param first_name: First name of the patient
        :param last_name: Last name of the patient
        :return: Http response of the API request
        """
        endpoint = "api/patients?first_name=%s&?last_name=%s" % (first_name, last_name)
        response = Doctor.api_request_drchrono(access_token, endpoint, "GET")
        return response

    @staticmethod
    def update_appointment(access_token, appointments):
        """
        Update the appointments information in the database,
        If the patient status is "Arrived", arrived_time filed will be append
        If the patient status is "Checked-in" or "In Room", waiting_time filed will be append
        Overwrite the given appointments
        :param access_token:Access_token of the user
        :param appointments:List of appointments
        :return:appointments():The updated appointments
        """
        require_waiting_time_status = ["Checked In", "In Room", "Complete", "In Session"]
        for a in appointments:
            patient_id = a.get('patient')
            scheduled_time = a.get('scheduled_time')
            appointment_id = a.get('id')
            appointment_saved = Appointment.objects.filter(appointment_id=appointment_id)
            if not appointment_saved:
                patient_info = Doctor.get_patient(access_token, patient_id)
                print "Get new appointment!"
                new_appointment = Appointment(appointment_id=str(appointment_id),
                                              duration=a.get('duration'),
                                              doctor_id=str(a.get('doctor')),
                                              scheduled_time=scheduled_time,
                                              patient_id=patient_id,
                                              patient_SSN=patient_info['social_security_number'],
                                              patient_first_name=patient_info['first_name'],
                                              patient_last_name=patient_info['last_name']
                                              )
                new_appointment.save()
            elif a.get('status') == "Arrived":
                try:
                    a['arrived_time'] = Appointment.objects.get(appointment_id=appointment_id).arrived_time
                except ObjectDoesNotExist:
                    a['arrived_time'] = None
            elif a.get('status') in require_waiting_time_status:
                try:
                    a['waiting_time'] = int(Appointment.objects.get(appointment_id=appointment_id).waiting_time) / 60
                except TypeError as e:
                    print "type error, waiting time is %s" % Appointment.objects.get(appointment_id=appointment_id).waiting_time
                    a['waiting_time'] = None
            else:
                # Todo handle other status
                pass
        # print "waiting time is ", Appointment.objects.get(appointment_id=69403988).waiting_time
        return appointments

    def update_average_waiting_time(self):
        """
        Update the average waiting time for the doctor given the historically appointments done in Kiosk
        :return:(Float)The average waiting time of the patients given the doctor(Not formatted)
        """
        appointments = Appointment.objects.filter(doctor_id=self.user_id)
        sum_time = 0
        counter = 0

        for a in appointments:
            if a.waiting_time is not None:
                sum_time += a.waiting_time
                counter += 1
        if counter:
            return sum_time / float(len(appointments))
        else:
            return self.average_waiting_time

    @staticmethod
    def update_appointment_status(access_token, appointment):
        """
        :param access_token: Access_token of the user
        :param appointment: Updated data of the appointment
        :return: (Boolean) True If the update operation success, False otherwise
        """
        endpoint = "api/appointments/%s" % appointment['id']
        response = Doctor.api_request_drchrono(access_token, endpoint, "PATCH", appointment, json_format=False)
        return response.status_code == 204

    @staticmethod
    def update_patient_demograph(access_token, patient_id, demograph):
        endpoint = "api/patients/%d" % int(patient_id)
        response = Doctor.api_request_drchrono(access_token, endpoint, "PATCH", demograph, json_format=False)
        return response.status_code == 204

    @staticmethod
    def get_appointment_status(access_token, appointment_id):
        """
        Get the appointment status for the given appointment
        :param access_token: Access_token of the user
        :param appointment_id: Id of the given appointment
        :return: (String)The status of the given appointment
        """
        endpoint = "api/appointments/%s" % appointment_id
        return Doctor.api_request_drchrono(access_token, endpoint, 'GET')['status']


class Appointment(models.Model):
    """
    Appointment should be created by Doctor
    Store the essential information about the appointment for retrieval
    waiting_time(Integer field in seconds) should only be changed when a doctor check in the patient of the appointment
    arrived_time filed should be set only once when the patient check in for that appointment
    """

    appointment_id = models.CharField(max_length=100, unique=True)
    doctor_id = models.IntegerField()
    scheduled_time = models.DateTimeField(default=timezone.now())
    duration = models.IntegerField()
    patient_id = models.CharField(max_length=100)
    patient_SSN = models.CharField(max_length=100)
    patient_first_name = models.CharField(max_length=100)
    patient_last_name = models.CharField(max_length=100)

    arrived_time = models.DateTimeField(null=True)
    waiting_time = models.IntegerField(null=True)

    #status = models.CharField(max_length=50) if we need to update status everytime and that will end up with an api call
    # no reason to store it locally

    def get_doctor_name(self):
        try:
            doctor_name = Doctor.objects.get(user_id=self.doctor_id).user
            return doctor_name

        except ObjectDoesNotExist:
            thepost = "Not found the doctor"

    def set_waiting_time(self, current_time):
        """
        :param current_time: The time patient stop waiting
        :return: the Appointment with the waiting time set
        """

        self.waiting_time = current_time
        return self


    @staticmethod
    def get_appointment_by_ssn(SSN):
        """
        :param SSN: SSN of the patient
        :return: the appointment object
        """
        appointment = Appointment.objects.filter(patient_SSN=SSN)
        return appointment

    @staticmethod
    def get_appointments_by_name(first_name, last_name):
        """
        :param first_name: First name of the patient
        :param last_name: Last name of the patient
        :return: the appointments for the patients today
        """
        # print Appointment.objects.filter(patient_first_name=u'Arielle',
        #                                  patient_last_name=u'Mandelberg',
        #                                  scheduled_time__day=18,
        #                                  scheduled_time__month=11,
        #                                  scheduled_time__year=2017)
        year, month, day = str(datetime.date.today()).split('-')
        appointments = Appointment.objects.filter(first_name=first_name,
                                                  last_name=last_name,
                                                  scheduled_time__day=day,
                                                  scheduled_time__month=month,
                                                  scheduled_time__year=year)
        return appointments
