

from re import A

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

class ContentDetailView(APIView):

    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not found."},404)
        return Response(model_to_dict(content), 200)
    
    def patch(self, request, content_id):
        errors = {}
        try: 
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not found."},404)


        for key, value in request.data.items():
            if type(value) is ContentSerializer.valid_inputs[key]:
                setattr(content, key, value)
            else:
                errors[key] = f'must be a {ContentSerializer.valid_inputs[key].__name__}'

        if errors:
            return Response(errors, 400)
        
        content.save()  
        return Response(model_to_dict(content), 200)

    def delete(self, request, content_id):
        try: 
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not found."},404)

        content.delete()
        return Response(status=204)
    
class ContentFilterView(APIView):
    def get(self, request):
        title_param = request.query_params.get("title")

        contents = Content.objects.filter(title__contains=title_param)

        filtered_contents = [model_to_dict(content) for content in contents]

        return Response(filtered_contents, 200)


