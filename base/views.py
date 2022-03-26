from .models import *
from django.shortcuts import render
import pandas as pd
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from pathlib import Path
from .models import *
from rest_framework.decorators import api_view
from django.db.models import DurationField, F, ExpressionWrapper
from datetime import datetime
from django.db.models import Q
import statistics
# Create your views here.
import numpy as np
import pandas as pd
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@csrf_exempt
@api_view(('GET', 'POST'))
def handleUpload(request):
    if request.method == 'POST':
        if request.data['main'] == 'backlog':
            priority = request.data['priority']
            Inctype = request.data['Inctype']
            obj = Backlog.objects.create(priority=priority, inc_type=Inctype)
            obj.save()
        elif request.data['main'] == 'raised':
            Resolution_date_time = request.data['Resolution_date_time'].replace(
                'T', ' ') + ":00+05"
            Creation_date_time = request.data['Creation_date_time'].replace(
                'T', ' ') + ":00+05"
            res_time = request.data['res_time']
            priority = request.data['priority']
            urgency = request.data['urgency']
            assigned_organization = request.data['assigned_organization']
            inc_type = request.data['inc_type']
            obj2 = Raised.objects.create(resolution_date_time=Resolution_date_time,
                                         creation_date_time=Creation_date_time,
                                         res_time=res_time,
                                         priority=priority,
                                         urgency=urgency,
                                         assigned_organization=assigned_organization,
                                         inc_type=inc_type)
            obj2.save()
        elif request.data['main'] == 'closed':
            Resolution_date_time = request.data['Resolution_date_time'].replace(
                'T', ' ') + ":00+05"
            Creation_date_time = request.data['Creation_date_time'].replace(
                'T', ' ') + ":00+05"
            priority = request.data['priority']
            obj3 = Closed.objects.create(resolution_date_time=Resolution_date_time,
                                         creation_date_time=Creation_date_time,
                                         priority=priority)
            obj3.save()

    return Response('success')


@api_view(('GET',))
def dashboard(request):
    all_raised = Raised.objects.all()
    one_closed_critica = Closed.objects.filter(priority='Critica').count()
    second_monthly_raised = Raised.objects.all().count()
    third_raised = {'alta': Raised.objects.filter(priority='Alta').count(), 'baja': Raised.objects.filter(priority='Baja').count(
    ), 'critica': Raised.objects.filter(priority='Crítica').count(), 'media': Raised.objects.filter(priority='Media').count()}

    four_backlog = {'alta': Backlog.objects.filter(priority='Alta').count(), 'baja': Backlog.objects.filter(priority='Baja').count(
    ), 'media': Backlog.objects.filter(priority='Media').count()}

    five_raised = {
        'access_failure': Raised.objects.filter(inc_type='ACCESS FAILURE').count(),
        'communications_failure': Raised.objects.filter(inc_type='COMMUNICATIONS FAILURE').count(),
        'data_issue': Raised.objects.filter(inc_type='DATA ISSUE').count(),
        'default': Raised.objects.filter(inc_type='DEFAULT').count(),
        'hardware_failure': Raised.objects.filter(inc_type='HARDWARE FAILURE').count(),
        'performance_issue': Raised.objects.filter(inc_type='PERFORMANCE ISSUE').count(),
        'printing_failure': Raised.objects.filter(inc_type='PRINTING FAILURE').count(),
        'process_failure': Raised.objects.filter(inc_type='PROCESS FAILURE').count(),
        'security_issue': Raised.objects.filter(inc_type='SECURITY ISSUE').count(),
        'security_issue_cyberattacks': Raised.objects.filter(inc_type='SECURITY ISSUE.CYBERATTACKS').count(),
        'software_failure': Raised.objects.filter(inc_type='SOFTWARE FAILURE').count(),
        'software_warning': Raised.objects.filter(inc_type='SOFTWARE WARNING').count(),
        'telephony_failure': Raised.objects.filter(inc_type='TELEPHONY FAILURE').count()}

    six_first = Raised.objects.filter(priority='Crítica')

    six_raised_critica_4_hour_per = 0

    for i in six_first:
        six_raised_critica_4_hour_per = six_raised_critica_4_hour_per+1
        # if ((i.resolution_date_time - i.creation_date_time).total_seconds()//3600 <= 4):
        #     if not (i.resolution_date_time - i.creation_date_time).total_seconds()//3600 < 0:

    seven_raised_priority_critica_per = 0

    eight = Raised.objects.filter(priority='Crítica')
    eight_raised_priority_per = 0

    for i in eight:
        if ((i.resolution_date_time - i.creation_date_time).total_seconds()//3600 >= 4):
            eight_raised_priority_per = eight_raised_priority_per + 1

    for i in eight:
        if ((i.resolution_date_time - i.creation_date_time).total_seconds()//3600 <= 4):
            seven_raised_priority_critica_per = seven_raised_priority_critica_per + 1

    nine_mean_critica = []

    for i in all_raised:
        if ((i.resolution_date_time - i.creation_date_time).total_seconds()//3600 <= 4) and i.priority == 'Crítica':
            if not (i.resolution_date_time - i.creation_date_time).total_seconds()//3600 < 0:
                nine_mean_critica.append(
                    (i.resolution_date_time - i.creation_date_time).total_seconds()//3600)

    return Response({'one_closed_critica': one_closed_critica, 'second_monthly_raised': second_monthly_raised, 'third_raised': third_raised, 'four_backlog': four_backlog, 'five_raised': five_raised, 'six_raised_critica_4_hour_per': six_raised_critica_4_hour_per, 'seven_raised_priority_critica_per': eight.count()//seven_raised_priority_critica_per * 100, 'eight_raised_priority_per': eight_raised_priority_per, 'nine_mean_critica': statistics.mean(nine_mean_critica)})


@api_view(['GET', 'POST'])
def signuppage(request):
    if request.method == "POST":
        try:
            username = request.data['username']
            email = request.data['email']
            password1 = request.data['password1']
            password2 = request.data['password2']
            f_name = request.data['f_name']
            l_name = request.data['l_name']
            user = User.objects.create_user(username=username.lower(
            ), email=email, password=password1, first_name=f_name, last_name=l_name)
            user.save()

            return Response({'status': 'success'})

        except:
            return Response({'status': 'failed'})


class ExportImportExcel(APIView):
    def post(self, request):
        exceled_upload_obj = ExcelFileUpload.objects.create(
            excel_file_upload=request.FILES['files'])
        df = pd.read_csv(
            f"{settings.BASE_DIR}/{exceled_upload_obj.excel_file_upload}")

        df.fillna('No Value', inplace=True)
        for student in (df.values.tolist()):
            try:
                Raised.objects.create(
                    creation_date_time=student[0],
                    resolution_date_time=student[1],
                    res_time=student[2],
                    priority=student[3],
                    urgency=student[4],
                    assigned_organization=student[5],
                    inc_type=student[6],
                )
            except:
                pass

        return Response("success")
