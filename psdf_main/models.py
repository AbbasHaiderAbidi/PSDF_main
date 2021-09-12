from django.db import models

# Create your models here.
class users(models.Model):
    username = models.CharField(max_length=200, null = False, unique = True)
    password = models.CharField(max_length=200, null = True)
    nodal = models.CharField(max_length=200, null = True)
    region = models.CharField(max_length=20, null = True)
    email = models.TextField(max_length=50, null=True)
    utilname = models.CharField(max_length=400, null = True)
    contact = models.CharField(max_length=10, null = True)
    address = models.CharField(max_length=500, null = True)
    reqdate = models.DateField(auto_now_add=True,null = True)
    aprdate = models.DateField( null = True)
    lastlogin = models.DateTimeField(null = True)
    admin = models.BooleanField(default=False)
    auditor = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    activate = models.BooleanField(default=False)
    notification = models.TextField(null=True)
    tpd = models.TextField(null=True)

class temp_projects(models.Model):
    userid = models.ForeignKey(users, null = True, on_delete = models.CASCADE)
    proname = models.CharField(max_length=200, null = True)
    dprsubdate = models.DateField(auto_now_add=True, null = True)
    dprdenydate = models.DateField(null = True, auto_now_add=True)
    amountasked = models.FloatField(null = True)
    projectpath = models.TextField(null = True)
    deny = models.BooleanField(max_length=1, null = True, default = False)
    remark = models.TextField(null = True)
    schedule = models.IntegerField(null = True)
    removed = models.BooleanField(max_length=1, null = True, default=False)
    submitted_boq  = models.TextField(null=True)

    def __str__(self):
        return self.username + " - " + self.proname


class projects(models.Model):
    userid = models.ForeignKey(users, null = True, on_delete = models.SET_NULL)
    name = models.CharField(max_length=200, null = False)
    newid = models.IntegerField(null = True, unique=True)
    dprsubdate = models.DateField(null = True)
    amt_asked = models.FloatField(null = False)
    amt_approved = models.FloatField(null = True)
    amt_released = models.FloatField(null = True)
    schedule = models.IntegerField(null = True)
    fundcategory = models.CharField(max_length=20, null = True)
    projectpath = models.TextField(null = True)
    quantumOfFunding = models.FloatField(null = True)
    status = models.CharField(max_length=1, null = True, default = '1')
    submitted_boq  = models.TextField(null=True)
    
    approved = models.BooleanField(default = False)
    deny = models.BooleanField(default = False)
    remark = models.TextField(null = True)
    
    denydate = models.DateField(null = True)
    approvedate = models.DateField(null = True)
    
    tesg_list = models.TextField(null=True)
    
    dpraprdate = models.DateField(null = True, auto_now_add=True)
    
    tesgaprdate = models.DateField(null = True)
    
    appraprdate = models.DateField(null = True)
    
    moniaprdate = models.DateField(null = True)
    
    finalaprdate= models.DateField(null = True)
    
    workflow = models.TextField(null=True)

    ##################################
    ## 1 - DPR approved
    ## 2 - TESG approved
    ## 3 - Appraisal approved
    ## 4 - Monitoring approved
    ## 5 - Final approval done
    ## 6 - Document Signing done
    ## 7 - Payment Done


class TESG_admin(models.Model):
    TESG_no = models.IntegerField(null=False, unique=True)
    filepath = models.TextField(null=True)
    TESG_date = models.DateField(null = True)
    projects = models.TextField(null=True)


class TESG_master(models.Model):
    project = models.ForeignKey(projects, null = True, on_delete= models.SET_NULL)
    tesgnum = models.ForeignKey(TESG_admin, null = True, on_delete=models.SET_NULL)
    user_response = models.TextField(null = True)
    user_filepath = models.TextField(null = True)
    user_res_date = models.DateField(null=True)
    admin_outcome = models.TextField(null = True)
    admin_filepath = models.TextField(null = True)
    active = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

class Appraisal_admin(models.Model):
    project = models.ForeignKey(projects, null = True, on_delete= models.SET_NULL)
    userid = models.ForeignKey(users, null = True, on_delete= models.SET_NULL)
    apprpath = models.TextField(null=True)
    apprdate = models.DateField(null = True)

class Monitoring_admin(models.Model):
    project = models.ForeignKey(projects, null = True, on_delete= models.SET_NULL)
    userid = models.ForeignKey(users, null = True, on_delete= models.SET_NULL)
    monipath = models.TextField(null=True)
    monidate = models.DateField(null = True)

class boqdata(models.Model):
    project = models.ForeignKey(projects, null = True, on_delete= models.CASCADE)
    boqtype = models.IntegerField(null=True)
    itemno = models.IntegerField(null = True)
    itemname = models.TextField(null=True)
    itemdesc = models.TextField(null=True)
    itemqty = models.IntegerField(null = True)
    unitcost = models.FloatField(null = True)

class loadata(models.Model):
    project = models.ForeignKey(projects, null = True, on_delete= models.CASCADE)
    tranche = models.IntegerField(null=True)
    req_boq = models.TextField(null=True)
    filepath = models.TextField(null=True)
    subdate = models.DateField(null = True, auto_now_add=True)
    compdate = models.DateField(null = True, auto_now_add=False)
    approved = models.CharField(max_length = 1, default = 2)
#1-- Completed
#2-- Ongoing
#3-- Rejected