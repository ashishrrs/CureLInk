from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery import Celery
from rest_framework.parsers import JSONParser
from rest_framework import authentication, permissions, status
from django.core.mail import send_mail
from django.conf import settings
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from celery.schedules import crontab
from django.http.response import HttpResponse
from django.shortcuts import render
import uuid
import json

from .models import *
from .serializers import *
import sys


@api_view(['GET'])
def get_article_list(request):
    article_objects = Article.objects.all().order_by('name')
    serializer = ArticleSerializer(article_objects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_article(request):
    data = JSONParser().parse(request)
    name = data.get('name', '')
    topic = data.get('topic', '')
    hours = data.get('hours', '')
    description = data.get('description', '')
    minutes = data.get('minutes', '')
    app = Celery('user_management')
    app.conf.enable_utc = False

    app.conf.update(timezone='Asia/Kolkata')
    crontab_objects = CrontabSchedule.objects.filter(
        hour=hours, minute=minutes).first()
    if crontab_objects is None:
        schedule, created = CrontabSchedule.objects.get_or_create(
            hour=hours, minute=minutes)
        task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_" +
                                           f"{uuid.uuid1()}", task='user_management.tasks.send_mail_func', one_off=True, args=json.dumps([hours, minutes]))
    if (name == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        c = Topic.objects.get_or_create(name=topic)[0]
        article = Article.objects.get_or_create(name=name,
                                                description=description, hours=hours, minutes=minutes,
                                                topic=c, published=0)
        return Response(status=status.HTTP_201_CREATED)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_subscriber_list(request):
    try:
        subscriber_objects = Subscriber.objects.all().order_by('name')
        serializer = SubscriberSerializer(subscriber_objects, many=True)
        return Response(serializer.data)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_subscriber(request):
    data = JSONParser().parse(request)
    name = data.get('name', '')
    email_id = data.get('email_id', '')
    phone_number = data.get('phone_number', '')
    topic = data.get('topic', '')
    if (name == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        c = Topic.objects.get_or_create(name=topic)[0]
        subscriber = Subscriber.objects.get_or_create(name=name,
                                                      email_id=email_id, phone=phone_number,
                                                      topic=c)
        return Response(status=status.HTTP_201_CREATED)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_topic_list(request):
    topic_objects = Topic.objects.all().order_by('name')
    serializer = TopicSerializer(topic_objects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_topic(request):
    data = JSONParser().parse(request)
    name = data.get('name', '')
    description = data.get('description', '')
    if (name == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        topic = Topic.objects.get_or_create(name=name,
                                            description=description)
        return Response(status=status.HTTP_201_CREATED)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_topic_list(request):
    topic_objects = Topic.objects.all().order_by('name')
    serializer = TopicSerializer(topic_objects, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def delete_topic(request):
    data = JSONParser().parse(request)
    id = data.get('id', '')
    if (id == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        topic = Topic.objects.filter(id=id).all()
        if topic is None:
            return Response("invalid id")
        topic.delete()
        return Response(status=status.HTTP_200_OK)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def delete_subscriber(request):
    data = JSONParser().parse(request)
    id = data.get('id', '')
    if (id == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        subscriber_object = Subscriber.objects.filter(id=id).all()
        if subscriber_object is None:
            return Response("invalid id")
        subscriber_object.delete()
        return Response(status=status.HTTP_200_OK)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def delete_article(request):
    data = JSONParser().parse(request)
    id = data.get('id', '')
    if (id == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        article_object = Article.objects.filter(id=id).all()
        if article_object is None:
            return Response("invalid id")
        article_object.delete()
        return Response(status=status.HTTP_200_OK)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_article(request):
    data = JSONParser().parse(request)
    id = data.get('id', '')
    name = data.get('name', '')
    topic = data.get('topic', '')
    hours = data.get('hour', '')
    app = Celery('user_management')
    app.conf.enable_utc = False

    app.conf.update(timezone='Asia/Kolkata')
    description = data.get('description', '')
    minutes = data.get('minutes', '')
    if (id == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        article_object = Article.objects.get(pk=id)
        if article_object is None:
            return Response("invalid id")
        c = Topic.objects.get_or_create(name=topic)[0]
        article_object.topic = c
        article_object.name = name
        if article_object.published == 0:
            crontab_objects = CrontabSchedule.objects.filter(
                hour=hours, minute=minutes).all()
            if crontab_objects is None:
                schedule, created = CrontabSchedule.objects.get_or_create(
                    hour=hours, minute=minutes)
                task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_" +
                                                   uuid.uuid1(), task='user_management.tasks.send_mail_func', one_off=True, args=json.dumps([hours, minutes]))
        article_object.hours = hours
        article_object.minutes = minutes
        article_object.description = description
        article_object.save()
        return Response(status=status.HTTP_200_OK)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_subscriber(request):
    data = JSONParser().parse(request)
    id = data.get('id', '')
    name = data.get('name', '')
    phone = data.get('phone', '')
    topic = data.get('topic', '')
    try:
        subscriber_object = Subscriber.objects.get(pk=id)
        if subscriber_object is None:
            return Response("invalid id")
        c = Topic.objects.get_or_create(name=topic)[0]
        subscriber_object.topic = c
        subscriber_object.name = name
        subscriber_object.phone = phone
        subscriber_object.save()
        return Response(status=status.HTTP_200_OK)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_topic(request):
    data = JSONParser().parse(request)
    id = data.get('id', '')
    name = data.get('name', '')
    description = data.get('description', '')
    if (id == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        topic_object = Topic.objects.get(pk=id)
        if topic_object is None:
            return Response("invalid id")
        topic_object.name = name
        topic_object.description = description
        topic_object.save()
        return Response(status=status.HTTP_200_OK)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_by_topic(request):
    data = JSONParser().parse(request)
    topic = data.get('topic', '')
    if (id == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        topic_object = Topic.objects.get(name=topic)
        if topic_object is None:
            return Response("invalid topic")
        article_objects = Article.objects.filter(topic=topic_object).all()
        serializer = ArticleSerializer(article_objects, many=True)
        return Response(serializer.data)

    except Exception as Arg:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(Arg)
        return Response({"exception": "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
