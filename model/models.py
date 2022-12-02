from django.db import models

class ingredients(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    protein = models.FloatField()
    energy = models.FloatField()
    lysine = models.FloatField()
    methionine = models.FloatField()
    e_extract = models.FloatField()
    c_fiber = models.FloatField()
    calcium = models.FloatField()
    phosphorus = models.FloatField()
    a_phosphorus = models.FloatField()
    pythic_phosphorus = models.FloatField()
    salt = models.FloatField()
    rate = models.FloatField()

class feeds(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    protein = models.FloatField()
    energy = models.FloatField()
    lysine = models.FloatField()
    methionine = models.FloatField()
    e_extract = models.FloatField()
    c_fiber = models.FloatField()
    calcium = models.FloatField()
    phosphorus = models.FloatField()
    a_phosphorus = models.FloatField()
    pythic_phosphorus = models.FloatField()
    salt = models.FloatField()

class optimize_log(models.Model):
    id = models.AutoField(primary_key=True)
    user_count = models.IntegerField()
    date = models.DateField()