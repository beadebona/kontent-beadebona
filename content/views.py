

from django.forms import model_to_dict
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView

from content.serializer import ContentSerializer

from .models import Content


class ContentView(APIView):
    def get(self, request):
        contents = Content.objects.all()
        content_list = []
        for content in contents:
            c = model_to_dict (content)
            content_list.append(c)
        return Response(content_list, 200)
    
    def post(self, request):
        new_content = ContentSerializer(**request.data)
        if new_content.is_valid():
            valid_content = Content.objects.create(**new_content.data)
            valid_content.save()
            content_dict = model_to_dict(valid_content)
            return Response(content_dict, 201)
        else:
            return Response(new_content.errors, 400)
        