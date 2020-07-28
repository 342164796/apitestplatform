from django.db import models

# Create your models here.


class Sign(models.Model):
    sign_id = models.AutoField(primary_key=True, null=False)
    sign_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.sign_name

class Project(models.Model):
    prj_id = models.AutoField(primary_key=True, null=False)
    prj_name = models.CharField(max_length=50)
    sign = models.ForeignKey('Sign', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.prj_name



class Environment(models.Model):
    env_id = models.AutoField(primary_key=True, null=False)
    env_name = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    private_key = models.CharField(max_length=50)

    def __str__(self):
        return self.env_name



class Interface(models.Model):
    if_id = models.AutoField(primary_key=True, null=False)
    if_name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    method = models.CharField(max_length=20)
    data_type = models.CharField(max_length=4)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    is_sign = models.IntegerField()
    description = models.CharField(max_length=100)
    request_header_param = models.TextField()
    request_body_param = models.TextField()
    response_header_param = models.TextField()
    response_body_param = models.TextField()

    def __str__(self):
        return self.if_name

class Case(models.Model):
    case_id = models.AutoField(primary_key=True, null=False)
    case_name = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.case_name

class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True, null=False)
    plan_name = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    environment = models.ForeignKey('Environment', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.plan_name

class Report(models.Model):
    report_id = models.AutoField(primary_key=True, null=False)
    report_name = models.CharField(max_length=255)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    content = models.TextField()
    case_num = models.IntegerField(null=True)
    pass_num = models.IntegerField(null=True)
    fail_num = models.IntegerField(null=True)
    error_num = models.IntegerField(null=True)

    def __str__(self):
        return self.report_name
class MonProject(models.Model):
    monprj_id = models.AutoField(primary_key=True, null=False)
    monprj_name = models.CharField(max_length=50)
    interview_time = models.IntegerField(null=True)

    def __str__(self):
        return self.monprj_name
class MonApi(models.Model):
    id=models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50)
    content = models.TextField()
    monprj = models.ForeignKey('MonProject', on_delete=models.CASCADE)
    time = models.IntegerField(null=True)
    status = models.IntegerField(null=True)
    details = models.TextField(null=True)

    def __str__(self):
        return self.name

class MonCfg(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    ding = models.TextField()
    jingmoqi = models.IntegerField(null=True)

    def __str__(self):
        return self.ding

class Alert(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    api_id =models.IntegerField(null=True)
    api_name = models.CharField(max_length=50)
    alert_details = models.TextField(null=True)
    alert_time = models.CharField(max_length=50)
    isAlert = models.IntegerField(null=True)
    count = models.IntegerField(null=True)
    def __str__(self):
        return self.id