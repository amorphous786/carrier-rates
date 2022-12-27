from rest_framework import serializers
from carriers.models import (Carriers,
                             ReportingPlan,
                             In_Network_File,
                             Allowed_Amount_File,
                             ReportingStructure,
                             TaxIdentifier,
                             Provider,
                             ProviderReference,
                             NegotiatedPrice,
                             NegotiatedRate,
                             BundledCode,
                             CoveredService,
                             InNetwork)
from django.core.files import File
import json
from rest_framework.response import Response
import os

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
    
class CarrierSerializer(serializers.ModelSerializer):
    
    json_file = serializers.FileField(write_only=True)
    reporting_structure = serializers.ListField(read_only=True)
 
    class Meta:
        model = Carriers
        fields = "__all__"
        read_only_fields = ['id','name','type',]
        
        
        
    def create(self,validated_data):

        file = validated_data
        json_file_ = File(file['json_file'],'rb')
        date = file['reporting_date']
        json_file = json.load(json_file_)
        
        in_network_path = "E:\\Downloads\\in_network\\" if os.name =='nt' else "~/Downloads/in_network"
        out_network_path = "E:\\Downloads\\out_network\\" if os.name =='nt' else "~/Downloads/out_network"
        reporting_plans_list = []
        in_network_files_list = []
        allowed_amount_files_list = []
        
        carrier = Carriers.objects.create(name=json_file["reporting_entity_name"],
                                        type=json_file["reporting_entity_type"],
                                        reporting_structure = [],
                                        reporting_date=date)
        
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
                        "path":in_network_path,
                        "document_status":'PENDING'})
                    
            if allowed_amount_files:
                # print(type("allowed_amount_files"))
                if isinstance(allowed_amount_files,list):
                    for allowed_amount_file in allowed_amount_files:
                        allowed_amount_files_list.append({"description":allowed_amount_file.get("description"),
                        "location":allowed_amount_file.get("location"),
                        "path":out_network_path,
                        "document_status":'PENDING' 
                        })
                    
                    
                else:
                    allowed_amount_files_list.append({"description":allowed_amount_files.get("description"),
                        "location":allowed_amount_files.get("location"),
                        "path":out_network_path,
                        "document_status":'PENDING' 
                        })   
            carrier.reporting_structure.append({"reporting_plans":reporting_plans_list,
                                                                "in_network_files":in_network_files_list,
                                                                "allowed_amount_file":allowed_amount_files_list })
            
            
            reporting_plans_list = []
            in_network_files_list = []
            allowed_amount_files_list = []
        carrier.save()
                        
        return carrier
            
    
class TaxIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxIdentifier
        fields = "__all__"