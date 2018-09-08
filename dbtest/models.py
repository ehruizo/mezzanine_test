from django.db import models
from datetime import timedelta, date
from django.utils import timezone


class Users(models.Model):
    document = models.IntegerField('Document', primary_key=True)
    first_name = models.CharField('First name', max_length=100)
    last_name = models.CharField('Last name', max_length=100)
    birth_date = models.DateField('Date of birth')

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class Invoices(models.Model):
    invoice = models.AutoField('Invoice number', primary_key=True)
    document = models.ForeignKey(Users, on_delete=models.CASCADE)
    invoice_date = models.DateTimeField('Date of purchase')

    def __str__(self):
        return str(self.invoice)

    def is_recent(self):
        return self.invoice_date >= timezone.now() - timedelta(days=5)


class Purchases(models.Model):
    invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE)
    product = models.CharField('Product', max_length=400)
    quantity = models.IntegerField('Quantity', default=0)
    price = models.FloatField('Price')

    def __str__(self):
        return '{}|{}'.format(self.invoice, self.product)


class Test(models.Model):
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('Value', max_length=400)

