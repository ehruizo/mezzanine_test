from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Sum, Count
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Users, Invoices, Test
from .forms import NewUserForm, NewInvoiceForm, NewProductForm, TestForm, AnalyticsForm
from datetime import datetime
import pytz
import json


localtz = pytz.timezone('America/Bogota')


def test1(request):
    return HttpResponse("hola, esto es una prueba")


def test2(request, par1, par2):
    get = json.dumps(request.GET)
    post = json.dumps(request.POST)
    cookies = json.dumps(request.COOKIES)
    meta_keys = request.META.keys()
    ip = request.META['REMOTE_ADDR']
    ua = request.META['HTTP_USER_AGENT']
    referer = request.META.get('HTTP_REFERER')
    proc = request.META.get('PROCESSOR_IDENTIFIER')
    user = request.user         # de authentication middleware
    session = request.session   # de session middleware (diccionario)
    sesskeys = session.keys()
    resp = """Parámetro 1: {}<br/><br/>Parámetro 2: {}<br/><br/>GET: {}<br/><br/>POST: {}<br/><br/>Cookies: {}<br/><br/>
    META: {}<br/><br/>IP: {}<br/><br/>User agent: {}<br/><br/>Referer: {}<br/><br/>User: {}<br/><br/>
    Procesador: {}<br/><br/>
    Session: {}<br/><br/>""".format(par1, par2, get, post, cookies, meta_keys, ip, ua, referer, user, proc, sesskeys)
    return HttpResponse(resp)


def test3(request):
    if request.is_ajax():                         # chequea si la petición es AJAX
        number = int(request.POST['number'])
        exists = Test.objects.filter(id=number).exists()
        message = "Warning: number already exists" if exists else ""
        return JsonResponse({"already_exists": exists, "message": message})     # retorna JSON
    elif request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            value = form.cleaned_data['value']
            Test(id=number, value=value).save()   # crea el registro o actualiza el valor si el id ya existe
            return HttpResponseRedirect(reverse('dbtest:test3'))
    else:
        form = TestForm()
    test_data = Test.objects.all()
    return render(request, 'dbtest/form_test.html', {'form': form, 'test_data': test_data})


def index(request):
    users = Users.objects.annotate(total_inv=Count('invoices__invoice')).order_by('-total_inv', 'last_name')
    context = {'user_list': users}
    return render(request, 'dbtest/index.html', context)


@login_required
def user_invoice(request, userid):
    user = get_object_or_404(Users, pk=userid)
    inv = user.invoices_set.all().order_by('-invoice').annotate(total_value=Sum('purchases__price'))
    context = {'inv_list': inv, 'user_data': user, 'age': user.get_age()}
    return render(request, 'dbtest/user_details.html', context)


@login_required
def invoice_details(request, invid):
    inv = get_object_or_404(Invoices, pk=invid)
    if request.method == 'POST':
        form = NewProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            inv.purchases_set.create(product=product, quantity=quantity, price=price)  # inserta en base de datos
            messages.add_message(request, messages.INFO, 'El producto "{}" fue agregado a la factura'.format(product))
            return HttpResponseRedirect(reverse('dbtest:invdetails', kwargs={'invid': invid}))
    else:
        form = NewProductForm()
    user = inv.document
    product_data = inv.purchases_set.all().order_by('-id')
    total_value = product_data.aggregate(value=Sum('price'))
    paginator = Paginator(product_data, 5)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'products': products, 'inv_data': inv, 'user_data': user, 'total_value': total_value, 'form': form}
    return render(request, 'dbtest/invoice_details.html', context)


@login_required
def delete_product(request, invid):
    if request.method == 'POST':
        purchase = int(request.POST.get('purchase_id'))
        invoice = get_object_or_404(Invoices, pk=invid)
        invoice.purchases_set.get(pk=purchase).delete()     # borra el registro de la base de datos
        messages.add_message(request, messages.INFO, 'El registro fue eliminado exitosamente')
    return HttpResponseRedirect(reverse('dbtest:invdetails', kwargs={'invid': invid}))


@login_required
def new_user(request):
    if request.method == 'POST':                    # form submitted
        form = NewUserForm(request.POST)            # bounded form (ready for validation)
        if form.is_valid():                         # check form data
            user = form.cleaned_data['document']
            if Users.objects.filter(document=user).exists():
                messages.add_message(request, messages.ERROR, 'El usuario {} ya existe!'.format(user))
            else:
                firstname = form.cleaned_data['first_name'].title()
                lastname = form.cleaned_data['last_name'].title()
                birthdate = form.cleaned_data['birth_date']
                Users(document=user, first_name=firstname, last_name=lastname, birth_date=birthdate).save()
                messages.add_message(request, messages.INFO, 'Usuario {} registrado exitosamente!'.format(user))
                return HttpResponseRedirect(reverse('dbtest:userinv', kwargs={'userid': user}))
        else:
            messages.add_message(request, messages.ERROR, 'El usuario no fue creado, corrija los errores!')
    else:
        form = NewUserForm()                         # form not submitted (unbounded)
    return render(request, 'dbtest/new_user.html', {'form': form})


@login_required
def new_invoice(request, userid):
    user = get_object_or_404(Users, pk=userid)
    if request.method == 'POST':
        form = NewInvoiceForm(request.POST)
        if form.is_valid():
            invoice_d = form.cleaned_data['invoice_d']
            invoice_t = form.cleaned_data['invoice_t']
            invoice_date = localtz.localize(datetime.combine(date=invoice_d, time=invoice_t))
            i = user.invoices_set.create(invoice_date=invoice_date)     # crea una nueva factura con el id autogenerado
            invoice = i.invoice                                         # número de la factura
            messages.add_message(request, messages.INFO, 'Factura creada exitosamente con número {}'.format(invoice))
            return HttpResponseRedirect(reverse('dbtest:invdetails', kwargs={'invid': invoice}))
        else:
            messages.add_message(request, messages.ERROR, 'Falló la creación de la factura!')
    else:
        form = NewInvoiceForm(initial={'invoice_d': datetime.today().date(), 'invoice_t': datetime.now().time()})
    return render(request, 'dbtest/new_invoice.html', {'user_data': user, 'form': form})


@login_required
def model_scorer(request):
    from .analytics import scorer
    if request.is_ajax():
        result = scorer(request.GET)
        return JsonResponse(result)
    form = AnalyticsForm(request.GET)
    if form.is_valid():
        result = scorer(form.cleaned_data)
    else:
        form = AnalyticsForm()
        result = {}
    return render(request, 'dbtest/scorer.html', {'score': result, 'form': form})


@login_required
def google_chart(request):
    if request.is_ajax():
        document = request.GET.get('document')
        if document == 'all':
            udata = Users.objects.annotate(total_val=Sum('invoices__purchases__price')).order_by('-total_val')
        else:
            document = int(document)
            udata = Users.objects.filter(document=document).annotate(total_val=Sum('invoices__purchases__price'))
        data = [['Cliente', 'Monto']]
        for u in udata:
            data.append([u.first_name, u.total_val])
        return JsonResponse({'data': data})
    users = Users.objects.all().order_by('first_name')
    return render(request, 'dbtest/charts.html', {'users': users})
