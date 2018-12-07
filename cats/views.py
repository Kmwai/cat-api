from .models import Cats
from .serializers import CatSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Cats API')
    return Response(generator.get_schema(request=request))


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_cat(request, pk):
    try:
        cat = Cats.objects.get(pk=pk)
    except Cats.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single cat
    if request.method == 'GET':
        serializer = CatSerializer(cat)
        return Response(serializer.data)
    # delete a cat
    if request.method == 'DELETE':
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # update a cat
    if request.method == 'PUT':
        serializer = CatSerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_cats(request):
    # get all cats
    if request.method == 'GET':
        cats = Cats.objects.all()
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data)
    # insert a new record
    elif request.method == 'POST':
        data = {
            'name': request.data.get('name'),
            'genus': request.data.get('genus'),
            'species': request.data.get('species'),
            'binomial_name': request.data.get('binomial_name')
        }
        serializer = CatSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)