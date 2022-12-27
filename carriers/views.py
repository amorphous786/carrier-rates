from .serializer import CarrierSerializer
from .models import Carriers
from rest_framework import viewsets,views
from rest_framework.response import Response
from rest_framework import status
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

class CarriersListAPI(views.APIView):
    def get(self,request,*args, **kwargs):
        carrier_name = kwargs.get('carrier_name')
        if not carrier_name:
            return Response({"Error":"Carrier Name not Passed"},status=status.HTTP_400_BAD_REQUEST)
        carriers = Carriers.objects.filter(name=carrier_name)
        serializer = CarrierSerializer(carriers,many=True)
        return Response(serializer.data)
    
    