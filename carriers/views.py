from .serializer import CarrierSerializer
from .models import Carriers
from rest_framework import viewsets,views
from rest_framework.response import Response

class CarriersViews(viewsets.ModelViewSet):
    """

    """
    serializer_class = CarrierSerializer
    queryset = Carriers.objects.all()

# class CarriersViews(views.APIView):
#     def get(self,request):
#         return Response({"yo":"I am working fine!"})
#         pass
#     def post(self,request):
#         serializer = CarrierSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response({"WORKING":'WORKING MAN'})
#         pass