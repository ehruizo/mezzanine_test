# python manage.py --database=apps_db inspectdb > modelsss.py
from __future__ import unicode_literals
from django.db import models


class DbtestUsers(models.Model):
    document = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'dbtest_users'


class DbtestInvoices(models.Model):
    invoice_date = models.DateTimeField()
    document = models.ForeignKey(DbtestUsers, models.CASCADE)
    invoice = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'dbtest_invoices'


class DbtestPurchases(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=400)
    quantity = models.IntegerField()
    price = models.FloatField()
    invoice = models.ForeignKey(DbtestInvoices, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'dbtest_purchases'


