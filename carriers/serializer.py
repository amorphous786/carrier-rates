from rest_framework import serializers
from carriers.models import Carriers,ReportingPlan,In_Network_File,Allowed_Amount_File,ReportingStructure
from django.core.files import File
import json
from rest_framework.response import Response


class InNetworkFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=In_Network_File
        fields = "__all__"
    
class AllowedAmountFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Allowed_Amount_File
        fields = "__all__"
class ReportingPlanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ReportingPlan
        fields = "__all__"

class ReportingStructure(serializers.Serializer):
    
    reporting_plans = serializers.ListField(read_only = True)
    in_network_files = serializers.ListField(read_only = True)
    allowed_amount_file = serializers.ListField(read_only = True)
    class Meta:
        model = ReportingStructure
        fields = "__all__"
    
class CarrierSerializer(serializers.Serializer):
    
    json_file = serializers.FileField(write_only=True)
    reporting_structure = serializers.ListField(read_only=True)
    class Meta:
        model = Carriers
        fields = "['json_file','name','type','reporting_structure']"
        
        
    def create(self,validated_data):

        file = validated_data
        json_file_ = File(file['json_file'],'rb')
       
        json_file = json.load(json_file_)
        

        reporting_plans_list = []
        in_network_files_list = []
        allowed_amount_files_list = []
        
        carrier = Carriers.objects.create(name=json_file["reporting_entity_name"],
                                        type=json_file["reporting_entity_type"],
                                        reporting_structure = [])
        
        for reporting_structure_object in json_file['reporting_structure']:
            reporting_plans = reporting_structure_object.get("reporting_plans",False)
            in_network_files = reporting_structure_object.get("in_network_files",False)
            allowed_amount_files = reporting_structure_object.get("allowed_amount_file",False)
            
            if reporting_plans:
                for reporting_plan in reporting_plans:

                    reporting_plans_list.append({"plan_name":reporting_plan.get("plan_name"),
                        "plan_type_id":reporting_plan.get("plan_id_type"),
                        "plan_id":reporting_plan.get("plan_id"),
                        "plan_market_type":reporting_plan.get("plan_market_type")
                        })
                    
            if in_network_files:
                for in_network_file in in_network_files:

                    in_network_files_list.append({"description":in_network_file.get("description"),
                        "location":in_network_file.get("location"),
                        "path":"E:\\Downloads\\in_network\\",
                        "document_status":'PENDING'})
                    
            if allowed_amount_files:
                allowed_amount_files_list.append({"description":allowed_amount_files.get("description"),
                    "location":allowed_amount_files.get("location"),
                    "path":"E:\\Downloads\\out_network\\",
                    "document_status":'PENDING' 
                    })
            
            carrier.reporting_structure.append({"reporting_plans":reporting_plans_list,
                                                                "in_network_files":in_network_files_list,
                                                                "allowed_amount_file":allowed_amount_files_list })
            
            carrier.save()
            reporting_plans_list = []
            in_network_files_list = []
            allowed_amount_files_list = []
        
        return Response({"Status":"Data Added Successfully!"})
                        
        return carrier
            
    