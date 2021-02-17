from django.db import models

# Create your models here.
class users(models.Model):
    username = models.CharField(max_length=200, null = False, unique = True)
    password = models.CharField(max_length=200, null = True)
    nodal = models.CharField(max_length=200, null = True)
    region = models.CharField(max_length=20, null = True)
    utilname = models.CharField(max_length=400, null = True)
    contact = models.CharField(max_length=10, null = True)
    address = models.CharField(max_length=500, null = True)
    reqdate = models.DateTimeField(null = True)
    aprdate = models.DateTimeField(auto_now_add=True, null = True)
    lastlogin = models.DateTimeField(null = True)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

class temp_projects(models.Model):
    userid = models.ForeignKey(users, null = True, on_delete = models.CASCADE)
    proname = models.CharField(max_length=200, null = True)
    dprsubdate = models.DateTimeField(auto_now_add=True, null = True)
    amountasked = models.FloatField(null = False)
    projectpath = models.CharField(max_length=600, null = True)
    deny = models.CharField(max_length=1, null = True)
    remark = models.CharField(max_length=1000, null = True)
    removed = models.CharField(max_length=1, null = True)


    def __str__(self):
        return self.username + " - " + self.proname


class projects(models.Model):

    userid = models.ForeignKey(users, null = True, on_delete = models.SET_NULL)
    name = models.CharField(max_length=200, null = False)
    dprsubdate = models.DateTimeField(null = True)
    dpraprdate = models.DateTimeField(null = True)
    amt_asked = models.FloatField(null = False)
    amt_approved = models.FloatField(null = False)
    amt_released = models.FloatField(null = False)
    schedule = models.IntegerField(null = True)
    fundcategory = models.CharField(max_length=20, null = True)
    projectpath = models.CharField(max_length=600, null = True)
    approved = models.CharField(max_length=1, null = True)
    remark = models.CharField(max_length=1000, null = True)
    status = models.CharField(max_length=1, null = True)
    ##################################
    ## 0 - Rejected
    ## 1 - DPR approved
    ## 2 - TESG
    ## 3 - Approval
    ## 4 - Monitoring
    ## 5 - Final approval
    ## 6 - Document Signed
    ## 7 - Payment
    
