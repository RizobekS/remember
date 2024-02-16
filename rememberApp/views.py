from decimal import Decimal
from pprint import pprint

from clickuz import ClickUz
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from payme.methods.generate_link import GeneratePayLink

from django.utils.translation import gettext_lazy as _

from rememberApp.forms import ContactForm, CalculateForm, FeedbackForm
from rememberApp.models import User, AboutPage, Services, CalculateCost, Feedback, Graveyard, Gallery, MyServices, Price
from transaction.service import initalize_transaction_click, initalize_transaction_payme



def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, _("Неправильный логин или пароль!"))
    return render(request, 'registration/login.html')


def register_view(request):
    if request.method == "POST":
        try:
            user = User()
            user.type = 3
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.phone = request.POST.get('phone')
            user.email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user.password = password1
                user.save()
            messages.success(request,
                             _("Вы успешно зарегистрировались!"))
            return redirect("login")
        except Exception as e:
            print(e)
            messages.error(request, _("Неправильный логин или пароль"))
    return render(request, "registration/register.html")


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    graveyard = Graveyard.objects.all().order_by('id')
    info_about = AboutPage.objects.first()
    approved_feedback = Feedback.objects.filter(approved=True).order_by('-date')
    if request.LANGUAGE_CODE == 'en':
        list_services = Services.objects.filter(english=True).order_by('-pk')
    elif request.LANGUAGE_CODE == 'ru':
        list_services = Services.objects.filter(russian=True).order_by('-pk')
    else:
        list_services = Services.objects.filter(uzbek=True).order_by('-pk')

    if request.method == "POST":
        form = CalculateForm(request.POST)
        if form.is_valid():
            form.save()
            name = request.POST['name']
            messages.success(request, 'Success!')
            return render(request, 'home.html',
                          {'name': name, 'services': list_services, 'approved_feedbacks': approved_feedback,
                           'graveyards': graveyard})
        else:
            name = _("Ooops something went wrong!")
            return render(request, 'home.html',
                          {'name': name, 'services': list_services, 'approved_feedbacks': approved_feedback,
                           'graveyards': graveyard})
    else:
        return render(request, "home.html",
                      {'services': list_services, 'info_about': info_about, 'approved_feedbacks': approved_feedback,
                       'graveyards': graveyard})


def cemeteries(request):
    if request.LANGUAGE_CODE == 'en':
        list_cemetery = Graveyard.objects.filter(english=True).order_by('-pk')
    elif request.LANGUAGE_CODE == 'ru':
        list_cemetery = Graveyard.objects.filter(russian=True).order_by('-pk')
    else:
        list_cemetery = Graveyard.objects.filter(uzbek=True).order_by('-pk')

    page = request.GET.get('page', 1)
    paginator = Paginator(list_cemetery, 10)  # number of news in each page

    try:
        list_cemetery = paginator.page(page)
    except PageNotAnInteger:
        list_cemetery = paginator.page(1)
    except EmptyPage:
        list_cemetery = paginator.page(paginator.num_pages)

    return render(request, "cemeteries.html", {"list_cemetery": list_cemetery})


def cemetery_details(request, pk):
    detail = Graveyard.objects.get(pk=pk)
    if request.LANGUAGE_CODE == 'en' and not detail.english:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/cemeteries/")
    elif request.LANGUAGE_CODE == 'uz' and not detail.uzbek:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/cemeteries/")
    elif request.LANGUAGE_CODE == 'ru' and not detail.russian:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/cemeteries/")
    similar_cemeteries = Graveyard.objects.exclude(pk=pk)

    return render(request, "cemetery-details.html", {'detail': detail, 'similar_cemeteries': similar_cemeteries})


def about(request):
    info_about = AboutPage.objects.first()
    return render(request, 'about_us.html', {'info_about': info_about})


def services(request):
    if request.LANGUAGE_CODE == 'en':
        list_services = Services.objects.filter(english=True).order_by('-pk')
    elif request.LANGUAGE_CODE == 'ru':
        list_services = Services.objects.filter(russian=True).order_by('-pk')
    else:
        list_services = Services.objects.filter(uzbek=True).order_by('-pk')

    page = request.GET.get('page', 1)
    paginator = Paginator(list_services, 30)  # number of news in each page

    try:
        list_services = paginator.page(page)
    except PageNotAnInteger:
        list_services = paginator.page(1)
    except EmptyPage:
        list_services = paginator.page(paginator.num_pages)

    return render(request, 'services.html', {'services': list_services})


def service_details(request, pk):
    detail = get_object_or_404(Services, pk=pk)
    price = Price.objects.filter(service=detail)
    if request.LANGUAGE_CODE == 'en' and not detail.english:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/services/")
    elif request.LANGUAGE_CODE == 'uz' and not detail.uzbek:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/services/")
    elif request.LANGUAGE_CODE == 'ru' and not detail.russian:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/services/")

    # increment views number by one every request
    detail.views += 1
    detail.save()

    return render(request, "service_details.html", {'detail': detail, 'price': price})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid() and request.POST['address'] == "":
            form.save()
            name = request.POST['name']
            messages.success(request, 'Success!')
            return render(request, 'contact.html', {'name': name})
        else:
            name = _("Ooops, something went wrong!")
            return render(request, 'contact.html', {'name': name})
    else:
        return render(request, 'contact.html', {})


def feedback(request):
    approved_feedback = Feedback.objects.filter(approved=True).order_by('-date')[:5]
    if request.LANGUAGE_CODE == 'en':
        list_services = Services.objects.filter(english=True).order_by('-pk')
    elif request.LANGUAGE_CODE == 'ru':
        list_services = Services.objects.filter(russian=True).order_by('-pk')
    else:
        list_services = Services.objects.filter(uzbek=True).order_by('-pk')

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            name = request.POST['name']
            messages.success(request, 'Success!')
            return render(request, 'feedback.html',
                          {'name': name, 'services': list_services, 'approved_feedback': approved_feedback})
        else:
            name = _("Ooops something went wrong!")
            return render(request, 'feedback.html',
                          {'name': name, 'services': list_services, 'approved_feedback': approved_feedback})
    else:
        return render(request, "feedback.html",
                      {'services': list_services, 'approved_feedback': approved_feedback})


def gallery(request):
    context = {
        'type_1': Gallery.objects.filter(type=0).order_by('-date'),
        'type_2': Gallery.objects.filter(type=1).order_by('-date'),
        'type_3': Gallery.objects.filter(type=2).order_by('-date'),
    }
    return render(request, 'gallery.html', context)


def dashboard(request):
    myservice = MyServices.objects.filter(user__id=request.user.id).order_by('-id')
    if request.method == 'POST':
        return redirect('services')

    context = {
        'myservice': myservice
    }

    return render(request, 'dashboard.html', context)


def invoice(request, id):
    myservice = MyServices.objects.get(id=id)

    context = {
        'myservice': myservice
    }
    return render(request, 'invoice_detail.html', context)


def myservicedetail(request, id):
    myservice = MyServices.objects.get(id=id)
    context = {
        'myservice': myservice
    }

    return render(request, 'myservice_detail.html', context)


@login_required(login_url='/login/')
def click_generate_url(request, amount, service_id):
    price = amount * 1

    transaction_id = initalize_transaction_click(
        request.user,
        price,
        service_id
    )

    generated_link = ClickUz.generate_url(
        order_id=transaction_id,
        amount=price,
        return_url='http://www.remember.uz/dashboard/'
    )
    return redirect(generated_link)


@login_required(login_url='/login/')
def payme_generate_url(request):
    amount = request.GET.get('amount')
    price_id = request.GET.get('price_id')
    res = float(amount) * float(100)
    price = Decimal(res)
    print(price)

    pay_link = GeneratePayLink(
        price_id,
        amount,

    ).generate_link()
    return redirect(pay_link)


def payment_success(request, payment_type, service_id, user):
    service = Services.objects.get(id=service_id)

    myservice = MyServices()
    myservice.user = user

    myservice.title_en = service.title_en
    myservice.title_ru = service.title_ru
    myservice.title_uz = service.title_uz

    myservice.description_en = service.description_en
    myservice.description_ru = service.description_ru
    myservice.description_uz = service.description_uz

    myservice.value = service.value  # price
    myservice.image = service.image
    myservice.image_2 = service.image_2
    myservice.image_3 = service.image_3
    myservice.image_4 = service.image_4

    myservice.payment_status = 'paid'
    myservice.payment_type = payment_type
    myservice.total_price = service.value
    myservice.save()

    return redirect('dashboard')

