from djongo import models
from mongoengine.fields import ListField
from django.db import models as dmodels
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
    
    # reporting_plans = models.EmbeddedField(model_container=ReportingPlan)
    # in_network_files = models.EmbeddedField(model_container=In_Network_File)
    # allowed_amount_file = models.EmbeddedField(model_container=Allowed_Amount_File)
    reporting_plans = models.ArrayField(model_container=ReportingPlan)
    in_network_files = models.ArrayField(model_container=In_Network_File)
    allowed_amount_file = models.ArrayField(model_container=Allowed_Amount_File)
    class Meta:
        abstract = True


class Carriers(models.Model):
    name = models.CharField(max_length=200,blank=False)
    type = models.CharField(max_length=200,blank=False)
    reporting_structure = models.ArrayField(model_container=ReportingStructure)
    
    objects = models.DjongoManager()

