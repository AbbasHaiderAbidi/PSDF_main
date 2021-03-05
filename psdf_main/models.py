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
    reqdate = models.DateTimeField(auto_now_add=True,null = True)
    aprdate = models.DateTimeField( null = True)
    lastlogin = models.DateTimeField(null = True)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    activate = models.BooleanField(default=False)
    notification = models.TextField(null=True)
    tpd = models.TextField(null=True)

class temp_projects(models.Model):
    userid = models.ForeignKey(users, null = True, on_delete = models.CASCADE)
    proname = models.CharField(max_length=200, null = True)
    dprsubdate = models.DateTimeField(auto_now_add=True, null = True)
    dprdenydate = models.DateTimeField(null = True)
    amountasked = models.FloatField(null = True)
    projectpath = models.TextField(max_length=600, null = True)
    deny = models.BooleanField(max_length=1, null = True, default = False)
    remark = models.CharField(max_length=1000, null = True)
    schedule = models.IntegerField(null = True)
    removed = models.BooleanField(max_length=1, null = True, default=False)
    submitted_boq  = models.TextField(null=True)
    

    def __str__(self):
        return self.username + " - " + self.proname


class projects(models.Model):

    userid = models.ForeignKey(users, null = True, on_delete = models.SET_NULL)
    name = models.CharField(max_length=200, null = False)
    dprsubdate = models.DateTimeField(null = True)
    dpraprdate = models.DateTimeField(null = True)
    amt_asked = models.FloatField(null = False)
    amt_approved = models.FloatField(null = True)
    amt_released = models.FloatField(null = True)
    schedule = models.IntegerField(null = True)
    fundcategory = models.CharField(max_length=20, null = True)
    projectpath = models.TextField(null = True)
    quantumOfFunding = models.FloatField(null = True)
    approved = models.CharField(max_length=1, null = False, default = '0')
    remark = models.TextField(null = True)
    extension = models.CharField(max_length = 1000, null = True)
    status = models.CharField(max_length=1, null = True, default = '1')
    approved_boq  = models.TextField(null=True)
    submitted_boq  = models.TextField(null=True)
    ##################################
    ## 0 - Rejected
    ## 1 - DPR approved
    ## 2 - TESG
    ## 3 - Appraisal
    ## 4 - Monitoring
    ## 5 - Final approval
    ## 6 - Document Signed
    ## 7 - Payment

class TESG(models.Model):
    projid = models.ForeignKey(projects, null = True, on_delete = models.CASCADE)
    total_TESG = models.IntegerField(null=True, default = 0)
    R_path_user = models.CharField(max_length = 1000, null  = True)
    R_path_admin = models.CharField(max_length = 1000, null  = True)
    status = models.CharField(max_length = 1000, null = True)
    comment = models.CharField(max_length = 1000, null = True)
    TESG_filepath = models.CharField(max_length = 1000, null = True)
    message = models.TextField(max_length = 200000, null = True) # stores a string of message communications admin - msg$user-msg$admin - msg
    complete = models.BooleanField(default=False, null=False) #set to True when admin approves from TESG
    tesg_open = models.BooleanField(default=False, null=False) # set true if admin files TESG, and false if user replies
    user_tesg_date = models.TextField(max_length =  20000, null = True)   #store like {'TESG1': ' 01-04-2021 ', 'TESG2' : '23-05-2021', .. , ..}
    admin_tesg_date = models.TextField(max_length = 20000, null = True)   #store like {'TESG1': ' 01-04-2021 ', 'TESG2' : '23-05-2021', .. , ..}
class monitoring(models.Model):
    projid =  models.ForeignKey(projects, null = True, on_delete = models.CASCADE)
    
    