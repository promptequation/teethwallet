import datetime
import json
import os
import random

from api.models.user_model import User
from appointment.models import Appointment
from auth_extend.models import *
from common.models import *
from dateutil import parser
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker


class Command(BaseCommand):
    '''
    Create Fake Doctor, Patient Data and The Superusers.
    Run: python manage.py sample
    50 doctor and 100 patient
    '''

    def create_superuser(self, username, password, email):
        users = User.objects.filter(username=username)
        num = len(users)
        if num:
            return
        User.objects.create_user(
            is_superuser=True,
            is_active=True,
            is_staff=True,
            username=username,
            password=password,
            email=email,
        )

    def handle(self, *args, **kwargs):
        self.create_superuser(
            username='admin1',
            password='1516',
            email='admin1@mail.com',
        )
        self.create_superuser(
            username='admin2',
            password='1516',
            email='admin2@mail.com',
        )
        self.create_superuser(
            username='admin3',
            password='1516',
            email='admin3@mail.com',
        )

        fake = Faker()
        name = fake.unique.name()
        text = fake.text()
        address = fake.address()
        date_of_birth = datetime.datetime.now().date()
        date_time = timezone.now()

        module_dir = os.path.dirname(__file__)
        doctors_file = os.path.join(module_dir, 'doctors.json')
        with open(doctors_file, 'r', encoding='utf-8') as f:
            doctors_data = json.loads(f.read())
            for doctor_data in doctors_data:
                doctor_first_name = doctor_data['first name']
                doctor_last_name = doctor_data['last name']
                doctor_name = f"{doctor_first_name} {doctor_last_name}"
                doctor = User.objects.create_user(
                    first_name=doctor_data['first name'], last_name=doctor_data['last name'], name=doctor_name,
                    date_of_birth=parser.parse(doctor_data['date of birth']), username=doctor_data['Username'],
                    email=doctor_data['email'], street=doctor_data['address'], nationality=doctor_data['nationality'],
                    language_code=doctor_data['language'],
                    city='Wellington', country=doctor_data['country'], password=doctor_data['password'],
                )
                doctor.save()
                doctor_user_group, created = Group.objects.get_or_create(
                    name='Doctor')
                if created:
                    doctor.groups.add(Group.objects.get(name='Doctor'))
                else:
                    doctor.groups.add(doctor_user_group)

        name = fake.unique.name()
        module_dir = os.path.dirname(__file__)
        patients_file = os.path.join(module_dir, 'patients.json')
        with open(patients_file, 'r', encoding='utf-8') as f:
            patients_data = json.loads(f.read())
            for patient_data in patients_data:
                patient_first_name = patient_data['first name']
                patient_last_name = patient_data['last name']
                patient_name = f"{patient_first_name} {patient_last_name}"
                patient = User.objects.create_user(
                    first_name=patient_data['first name'], last_name=patient_data['last name'], name=patient_name,
                    date_of_birth=parser.parse(patient_data['date of birth']), username=patient_data['Username'],
                    email=patient_data['email'], street=patient_data['address'],
                    nationality=patient_data['nationality'], language_code=patient_data['language'],
                    city='Wellington', country=patient_data['country'], password=patient_data['password'],
                )
                patient.save()
                patient_user_group, created = Group.objects.get_or_create(
                    name='Patient')
                if created:
                    patient.groups.add(Group.objects.get(name='Patient'))
                else:
                    patient.groups.add(patient_user_group)

        no = random.randint(1, 100)
        doctors = User.objects.filter(groups__name='Doctor')
        patients = User.objects.filter(groups__name='Patient')
        specializations = Specialization.objects.all()
        qualifications = Qualification.objects.all()
        lookuptypes = LookUpType.objects.all()
        lookups = LookUp.objects.all()
        companies = Company.objects.all()
        appointments = Appointment.objects.all()
        questions = Question.objects.all()
        question_responses = QuestionResponse.objects.all()
        priorities = Priority.objects.all()
        currentdate = datetime.datetime.now(tz=timezone.utc)

        for doctor in doctors:
            doctor_fisrt_name = doctor.first_name
            doctor_last_name = doctor.last_name
            company_name = f"{doctor_fisrt_name} {doctor_last_name}"
            company = Company(code=doctor.first_name, name=company_name, street=address, street2=fake.address(),
                              state=fake.state(), city=fake.city(),
                              zipcode=fake.zipcode(), country='NZ', created_by=doctor, updated_by=doctor)
            company.save()

        # for company in companies[:5]:
        #     for d in doctors:
        #         for p in patients:
        #             appointment = Appointment(patient=patient, doctor=d, company=company, start_date=currentdate, duration=10, created_by=patient, updated_by=doctor)
        #             appointment.save()

        duration_numbers = [10, 20, 30, 40, 50, 60, 60, 70, 80, 90]
        for duration_number in duration_numbers:
            duration = Duration(number=duration_number,
                                created_by=patient, updated_by=doctor)
            duration.save()

        teeth_file = os.path.join(module_dir, 'teeth.txt')
        teeth_data = open(teeth_file, 'r')
        tooth_numbers = []
        for line in teeth_data:
            tooth_numbers.append(line.strip())
        for tooth_number in tooth_numbers:
            tooth = Tooth(number=tooth_number,
                          created_by=patient, updated_by=doctor)
            tooth.save()

        # treatments_file = os.path.join(module_dir, 'treatments.txt')
        # treatments_data = open(treatments_file, 'r')
        # treatments_names = []
        # for line in treatments_data:
        #     treatments_names.append(line.strip())
        # for treatment_name in treatments_names:
        #     treatment = Treatment(name=treatment_name,
        #                           created_by=patient, updated_by=doctor)
        #     treatment.save()

        # diagnostic_file = os.path.join(module_dir, 'diagnostics.txt')
        # diagnostic_data = open(diagnostic_file, 'r')
        # diagnostic_names = []
        # for line in diagnostic_data:
        #     diagnostic_names.append(line.strip())
        # for diagnostic_name in diagnostic_names:
        #     diagnostic = Diagnostic(
        #         name=diagnostic_name, created_by=patient, updated_by=doctor)
        #     diagnostic.save()

        specialization_names = [
            'Endodontics and Operative Dentistry', 'Oral Surgery and Oral Medicine', 'Oral & Maxillofacial Radiology',
            'Orthodontics and Dentofacial Orthopedics', 'Prosthodontics and Occlusion', 'Periodontics',
            'Pediatric Dentistry',
            'Preventive Dentistry and Oral Hygiene',
        ]
        for specialization_name in specialization_names:
            specialization = Specialization(
                name=specialization_name, created_by=patient, updated_by=doctor)
            specialization.save()

        for s in specializations:
            userSpecialization = UserSpecialization(
                user=patient, specialization=s)
            userSpecialization.save()

        qualify_names = ['MBBS', 'BAMS', 'MS', 'MD',
                         'BHMS', 'BPT', 'BUMS', 'BSMS', 'BNYS', 'B.VSc']
        for qualify_name in qualify_names:
            qualify = Qualification(
                name=qualify_name, created_by=patient, updated_by=doctor)
            qualify.save()

        for q in qualifications:
            userQualification = UserQualification(
                user=patient, qualification=q)
            userQualification.save()

        codes = ["TITLE", "APPROVAL", "BLOOD_GROUP",
                 "ELEMENT_TYPE", 'DECISION_STATUS']
        for code in codes:
            lookUpType = LookUpType(
                code=code, created_by=patient, updated_by=doctor)
            lookUpType.save()

        decisions = ['Yes', 'No']
        titles = ["Mr", "Mrs", "Miss", "Ms", "Mx"]
        titles_code = ["MX", "MS", "MIS", "MRS", "MR"]
        approvals = ["Approve", "Reject", "Pending"]
        elements = ["CHECK_BOX", "RADIO_BUTTON", "TEXT_BOX"]
        blood_groups = ["A positive (A+)", "A negative (A-)", "B positive (B+)", "B negative (B-)", "O positive (O+)",
                        "O negative (O-)", "AB positive (AB+)", "AB negative (AB-)"]
        blood_groups_code = ["AP", "AN", "BP", "BN", "OP", "ON", "ABP", "APN"]
        for lookup in lookuptypes:
            for element in elements:
                if lookup.code == "ELEMENT_TYPE":
                    lookUps = LookUp(name=element, group=lookup, code=name, description=text, created_by=patient,
                                     updated_by=doctor)
                    lookUps.save()
        for lookup in lookuptypes[:4]:
            for title in titles:
                for title_code in titles_code:
                    if lookup.code == "TITLE":
                        lookUps = LookUp(name=title, group=lookup, code=title_code, description=text,
                                         created_by=patient, updated_by=doctor)
                        lookUps.save()
        for lookup in lookuptypes[:4]:
            for approve in approvals:
                if lookup.code == "APPROVAL":
                    lookUps = LookUp(name=approve, group=lookup, code=name, description=text, created_by=patient,
                                     updated_by=doctor)
                    lookUps.save()
        for lookup in lookuptypes[:4]:
            for blood_group in blood_groups:
                for blood_group_code in blood_groups_code:
                    if lookup.code == "BLOOD_GROUP":
                        lookUps = LookUp(name=blood_group, group=lookup, code=blood_group_code, description=text,
                                         created_by=patient, updated_by=doctor)
                        lookUps.save()
        for lookup in lookuptypes[:5]:
            for decision in decisions:
                if lookup.code == "DECISION_STATUS":
                    lookUps = LookUp(name=decision, group=lookup, code=name, description=text, created_by=patient,
                                     updated_by=doctor)
                    lookUps.save()

        for status in lookups:
            if status.name == "Approve":
                for company in companies:
                    for doctor in doctors:
                        if company.created_by == doctor:
                            company_user = CompanyUser(company=company, group=doctor_user_group, user=doctor,
                                                       is_owner=True, status=status,
                                                       joined_datetime=date_time, approval_at=date_time)
                            company_user.save()

        for status in lookups:
            if status.name == "Approve":
                for company in companies:
                    for doctor in doctors:
                        for patient in patients:
                            if company.created_by == doctor:
                                if patient.username == "Eduardo" and doctor.username == "Joana":
                                    company_user = CompanyUser(company=company, group=patient_user_group, user=patient,
                                                               doctor=doctor, is_owner=False, status=status,
                                                               joined_datetime=date_time, approval_at=date_time,
                                                               requested_by=patient, approval_by=doctor,
                                                               is_active=False)
                                    company_user.save()

                                if patient.username == "Eduardo" and doctor.username == "Marcus":
                                    company_user = CompanyUser(company=company, group=patient_user_group, user=patient,
                                                               doctor=doctor, is_owner=False, status=status,
                                                               joined_datetime=date_time, approval_at=date_time,
                                                               requested_by=patient, approval_by=doctor,
                                                               is_active=False)
                                    company_user.save()

                                if patient.username == "Susan" and doctor.username == "Hugo":
                                    company_user = CompanyUser(company=company, group=patient_user_group, user=patient,
                                                               doctor=doctor, is_owner=False, status=status,
                                                               joined_datetime=date_time, approval_at=date_time,
                                                               requested_by=patient, approval_by=doctor,
                                                               is_active=False)
                                    company_user.save()

                                if patient.username == "Albert" and doctor.username == "Benedict":
                                    company_user = CompanyUser(company=company, group=patient_user_group, user=patient,
                                                               doctor=doctor, is_owner=False, status=status,
                                                               joined_datetime=date_time, approval_at=date_time,
                                                               requested_by=patient, approval_by=doctor,
                                                               is_active=False)
                                    company_user.save()

                                if patient.username == "Telma" and doctor.username == "Marie":
                                    company_user = CompanyUser(company=company, group=patient_user_group, user=patient,
                                                               doctor=doctor, is_owner=False, status=status,
                                                               joined_datetime=date_time, approval_at=date_time,
                                                               requested_by=patient, approval_by=doctor,
                                                               is_active=False)
                                    company_user.save()

                                if patient.username == "bruno31" and doctor.username == "Anne":
                                    company_user = CompanyUser(company=company, group=patient_user_group, user=patient,
                                                               doctor=doctor, is_owner=False, status=status,
                                                               joined_datetime=date_time, approval_at=date_time,
                                                               requested_by=patient, approval_by=doctor,
                                                               is_active=False)
                                    company_user.save()

                                if patient.username == "antonio2" and doctor.username == "Harry":
                                    company_user = CompanyUser(company=company, group=patient_user_group, user=patient,
                                                               doctor=doctor, is_owner=False, status=status,
                                                               joined_datetime=date_time, approval_at=date_time,
                                                               requested_by=patient, approval_by=doctor,
                                                               is_active=False)
                                    company_user.save()

                                if patient.username == "antonio2" and doctor.username == "Esme":
                                    company_user = CompanyUser(company=company, group=patient_user_group, user=patient,
                                                               doctor=doctor, is_owner=False, status=status,
                                                               joined_datetime=date_time, approval_at=date_time,
                                                               requested_by=patient, approval_by=doctor,
                                                               is_active=False)
                                    company_user.save()

                                if patient.username == "carol1" and doctor.username == "Kyle":
                                    company_user = CompanyUser(company=company, group=patient_user_group, user=patient,
                                                               doctor=doctor, is_owner=False, status=status,
                                                               joined_datetime=date_time, approval_at=date_time,
                                                               requested_by=patient, approval_by=doctor,
                                                               is_active=False)
                                    company_user.save()

                                if patient.username == "rui" and doctor.username == "Joe":
                                    company_user = CompanyUser(company=company, group=patient_user_group, user=patient,
                                                               doctor=doctor, is_owner=False, status=status,
                                                               joined_datetime=date_time, approval_at=date_time,
                                                               requested_by=patient, approval_by=doctor,
                                                               is_active=False)
                                    company_user.save()

        # for _ in range(1):
        #     for lookup in lookups:
        #         if lookup.name == "Approve":
        #             for company in companies:
        #                 for doctor in doctors:
        #                     companyUser = CompanyUser(company=company, group=doctor_user_group, user=doctor, doctor=doctor, is_active=False, status=lookup,
        #                     joined_datetime=date_time, requested_by=doctor, approval_at=date_time, approval_by=doctor)
        #                     companyUser.save()

        for _ in range(10):
            doctorType = DoctorType(type=fake.first_name(
            ), code=fake.name(), created_by=patient, updated_by=doctor)
            doctorType.save()

        # for a in appointments:
        #     appointment_detail = AppointmentDetail(appointment=a, tooth=tooth, treatment=treatment,
        #                                            diagnosis=diagnostic, created_by=patient, updated_by=doctor)
        #     appointment_detail.save()

        question_title = ['Heart Problems?']
        reference_id = 999
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No", "I Don't know"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Kidney diseases?']
        reference_id = 1000
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No", "I Don't know"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        for _ in range(1):
            reference_id = 1001
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title='Are you taking any medication?', reference_id=reference_id,
                                        serial_no=reference_id, is_conditional_question=False, element_type=lookup,
                                        created_by=patient, updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No"]
        reference_id = 0
        for responses_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=responses_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        for _ in range(1):
            reference_id = 1002
            for lookup in lookups:
                if lookup.name == "TEXT_BOX":
                    reference_id += 1
                    question = Question(title='Please type the name of your medication?', reference_id=reference_id,
                                        serial_no=reference_id, is_conditional_question=True, element_type=lookup,
                                        created_by=patient, updated_by=doctor)
                    question.save()

        question_title = ['Diabetes?']
        reference_id = 1003
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No", "I Don't know"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Hypertension?']
        reference_id = 1004
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No", "I Don't know"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Do you have any infectious diseases?']
        reference_id = 1005
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Please select your diseases']
        reference_id = 1006
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=True, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Hepatitis",
                                    "Tuberculosis", "HIV", "Syphilis", "Other"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Which type of hepatitis disease it is?']
        reference_id = 1007
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "TEXT_BOX":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=True, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_title = ['Please type your others diseases']
        reference_id = 1008
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "TEXT_BOX":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=True, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_title = ['Blood diseases?']
        reference_id = 1009
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Please select your blood diseases']
        reference_id = 1010
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "CHECK_BOX":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=True, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Anemia", "Hemophilia", "Other"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Please type the name of your blood diseases?']
        reference_id = 1011
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "TEXT_BOX":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=True, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_title = ['Liver diseases?']
        reference_id = 1012
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No", "I Don't know"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Stomach diseases?']
        reference_id = 1013
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No", "I Don't know"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Are you a smoker?']
        reference_id = 1014
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Do you have epilepsy?']
        reference_id = 1015
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = [
            'Are you, or have you been under radio/chemotherapy treatment?']
        reference_id = 1016
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = [
            'Are you allergic to any medicine or medical device?']
        reference_id = 1017
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = ['Please select your medicine or medical device name']
        reference_id = 1018
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "CHECK_BOX":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=True, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Aspirin", "Sulfamides", 'Anesthetics', 'Penicillins', 'Tetracyclines', 'Nichel',
                                    'Chromium/Cobalt', 'Acrylic', 'Latex', 'Others']
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        question_title = [
            'Please type the name of your medicine or medical device']
        reference_id = 1019
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "TEXT_BOX":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=True, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_title = [
            'Are there diseases in the family such as cancer, diabetes, cardiac and allergies?']
        reference_id = 1020
        for title in question_title:
            for lookup in lookups:
                if lookup.name == "RADIO_BUTTON":
                    reference_id += 1
                    question = Question(title=title, reference_id=reference_id, serial_no=reference_id,
                                        is_conditional_question=False, element_type=lookup, created_by=patient,
                                        updated_by=doctor)
                    question.save()

        question_responses_title = ["Yes", "No"]
        reference_id = 0
        for response_title in question_responses_title:
            reference_id += 1
            question_responses = QuestionResponse(title=response_title, question=question, reference_id=reference_id,
                                                  serial_no=reference_id, created_by=patient, updated_by=doctor)
            question_responses.save()

        priority_names = [
            '1st dental consultation', 'Dental consultation',
            'Consultation for presentation and discussion of treatment plan', 'Revaluation consultation',
            'Emergency consultation at night time (9:00 pm to 8:00 am) on weekends or holidays', 'Urgent consultation',
            'Home consultation', 'Home travel'
        ]
        for priority_name in priority_names:
            priority = Priority(name=priority_name,
                                created_by=patient, updated_by=doctor)
            priority.save()

        # for priority in  priorities[:5]:
        #     for apnts in appointments[:5]:
        #         appointment_priority = AppointmentPriority(appointment=apnts, priority=priority, created_by=patient, updated_by=doctor)
        #         appointment_priority.save()
