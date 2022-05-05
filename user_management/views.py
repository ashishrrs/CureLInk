from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import authentication, permissions, status
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
    notification_time = data.get('notification_time', '')
    description = data.get('description', '')
    if (name == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        c = Topic.objects.get_or_create(name=topic)[0]
        article = Article.objects.get_or_create(name=name,
                                                description=description, notification_time=notification_time,
                                                topic=c)
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
    notification_time = data.get('notification_time', '')
    description = data.get('description', '')
    if (id == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        article_object = Article.objects.get(pk=id)
        if article_object is None:
            return Response("invalid id")
        c = Topic.objects.get_or_create(name=topic)[0]
        article_object.topic = c
        article_object.name = name
        article_object.notification_time = notification_time
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
