from djongo import models
# from mongoengine.fields import ListField

# from django_mongoengine import Document,EmbeddedDocument,fields
ENUM_DOWNLOAD_STATUS = (('COMPLETED','completed'),
                        ('PENDING','pending'),
                        ('IN_PROGRESS','in_progress'),
                        ('FAILED','failed')
                        )

class ReportingPlan(models.Model):

    plan_name = models.CharField(max_length=250,blank=False)
    plan_type_id = models.CharField(max_length=200,blank=False)
    plan_id = models.CharField(max_length=200,blank=False)
    plan_market_type = models.CharField(max_length=200,blank=False)
    class Meta:
        abstract = True
        
class In_Network_File(models.Model):
    description = models.CharField(max_length=1000,blank=False,default="in-network file")
    location = models.TextField(blank=False)
    path = models.CharField(max_length=1000,blank=False,default="E:\\Downloads\\in_network\\")
    document_status = models.CharField(max_length=15,choices=ENUM_DOWNLOAD_STATUS,default="PENDING")
    class Meta:
        abstract = True

class Allowed_Amount_File(models.Model):
    description = models.CharField(max_length=1000,blank=False,default='allowed amount file')
    location = models.TextField(blank=False)
    path = models.CharField(max_length=1000,blank=False,default="E:\\Downloads\\allowed_amount\\")
    document_status = models.CharField(max_length=15,choices=ENUM_DOWNLOAD_STATUS,default="PENDING")
    class Meta:
        abstract = True

class ReportingStructure(models.Model):
    
    
    reporting_plans = models.ArrayField(model_container=ReportingPlan)
    in_network_files = models.ArrayField(model_container=In_Network_File)
    allowed_amount_file = models.ArrayField(model_container=Allowed_Amount_File)
    class Meta:
        abstract = True


class Carriers(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200,blank=False)
    type = models.CharField(max_length=200,blank=False)
    reporting_structure = models.ArrayField(model_container=ReportingStructure)
    reporting_date = models.DateField()
    objects = models.DjongoManager()
##################################################################
#####################IN NETWORK FILES DATA MODEL/TABLE############
##################################################################



#To create tin object in Provider model
class TaxIdentifier(models.Model):
    type = models.CharField(max_length=1000,blank=False)
    value = models.CharField(max_length=1000,blank=False)
    class Meta:
        abstract = True

#To be used in Negotiated rate to create objects for the provider group also in ProviderReference
class Provider(models.Model):
    npi = models.JSONField()
    tin = models.EmbeddedField(model_container=TaxIdentifier)
    class Meta:
        abstract = True

#Provider Reference for provider_references array in NegotiatedRate model 
class ProviderReference(models.Model):
    provider_group_id = models.BigIntegerField()
    provider_groups = models.ArrayField(model_container=Provider)
    location = models.TextField(blank=True,null=True)
    class Meta:
        abstract = True
        


#To be used in NegotiatedRate model for creating negotiated_price
class NegotiatedPrice(models.Model):
    negotiated_type = models.CharField(max_length=1000,blank=False)
    negotiated_rate = models.IntegerField(blank=False)
    expiration_date = models.CharField(max_length=1000,blank=False)
    service_code = models.JSONField()
    billing_class = models.CharField(max_length=1000,blank=True,null=True)
    billing_code_modifier = models.JSONField()
    additional_information = models.CharField(max_length=1000,blank=False)
    class Meta:
        abstract = True

#To be used in InNetwork model for creating negotiated rates array
class NegotiatedRate(models.Model):
    negotiated_prices = models.ArrayField(model_container=NegotiatedPrice)
    provider_groups = models.ArrayField(model_container=Provider)
    provider_references = models.ArrayField(model_container=ProviderReference)
    class Meta:
        abstract = True
#BundledCode to be used in InNetwork model 
class BundledCode(models.Model):
    billing_code_type = models.TextField()
    billing_code_type_version = models.TextField()
    billing_code = models.TextField()
    description = models.TextField()
    class Meta:
        abstract = True
#CoveredService to be used in InNetwork model 
class CoveredService(models.Model):
    billing_code_type = models.TextField()
    billing_code_type_version = models.TextField()
    billing_code = models.TextField()
    description = models.TextField()
    class Meta:
        abstract=True        
#To be used to create in-network object inside the in_network array
class InNetwork(models.Model):
    negotiation_arrangement = models.CharField(max_length=1000,blank=False)
    name = models.CharField(max_length=1000,blank=False)
    billing_code_type = models.CharField(max_length=1000,blank=False)
    billing_code_type_version  =models.CharField(max_length=1000,blank=False)
    billing_code = models.CharField(max_length=1000,blank=False)
    description = models.CharField(max_length=1000,blank=False)
    negotiated_rates = models.ArrayField(model_container=NegotiatedRate)
    bundled_codes = models.ArrayField(model_container=BundledCode)
    covered_services = models.ArrayField(model_container=CoveredService)
    
    class Meta:
        abstract = True
        
#In-Network's file data will follow this model
class InNetworkFileData(models.Model):
    id = models.BigAutoField(primary_key=True)    
    reporting_entity_name = models.CharField(max_length=1000,blank=False)
    reporting_entity_type = models.CharField(max_length=1000,blank=False)
    plan_name = models.CharField(max_length=1000,blank=True,null=True)
    plan_id_type = models.CharField(max_length=1000,blank=True,null=True)
    plan_market_type = models.CharField(max_length=1000,blank=True,null=True)
    in_network = models.ArrayField(model_container=InNetwork)
    provider_references = models.ArrayField(model_container=ProviderReference)
    last_updated_on = models.CharField(max_length=1000,blank=True,null=True)
    version = models.CharField(max_length=1000,blank=False)
    
