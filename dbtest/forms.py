from django import forms
from datetime import datetime


dformats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']


class NewUserForm(forms.Form):
    document = forms.IntegerField(min_value=1, label='Documento')
    first_name = forms.CharField(min_length=2, label='Nombre')
    last_name = forms.CharField(min_length=2, label='Apellido')
    birth_date = forms.DateField(input_formats=dformats, label='Fecha de nacimiento',
                                 widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'class': 'form-control'}))

    def clean_birth_date(self):
        data = self.cleaned_data['birth_date']
        if data > datetime.today().date():
            raise forms.ValidationError("La fecha no puede ser mayor a hoy")
        return data


class NewInvoiceForm(forms.Form):
    invoice_d = forms.DateField(input_formats=dformats, label='Fecha')
    invoice_t = forms.TimeField(label='Hora')


class NewProductForm(forms.Form):
    product = forms.CharField(min_length=1, label='Producto')
    quantity = forms.IntegerField(min_value=1, label='Cantidad', initial=1)
    price = forms.FloatField(min_value=0, label='Valor total')


class TestForm(forms.Form):
    number = forms.IntegerField(label='ID')
    value = forms.CharField(label='Value')


class AnalyticsForm(forms.Form):
    sepal_length = forms.FloatField(label="Sepal length", widget=forms.NumberInput(attrs={'step': '0.1'}))
    sepal_width = forms.FloatField(label="Sepal width", widget=forms.NumberInput(attrs={'step': '0.1'}))
    petal_length = forms.FloatField(label="Petal length", widget=forms.NumberInput(attrs={'step': '0.1'}))
    petal_width = forms.FloatField(label="Petal width", widget=forms.NumberInput(attrs={'step': '0.1'}))

