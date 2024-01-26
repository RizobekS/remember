from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.utils.translation import gettext_lazy as _

from rememberApp.forms import ContactForm, CalculateForm, FeedbackForm
from rememberApp.models import AboutPage, Services, CalculateCost, Feedback, Graveyard


def home(request):
    graveyard = Graveyard.objects.all()
    info_about = AboutPage.objects.first()
    approved_feedback = CalculateCost.objects.filter(approved=True).order_by('-date')
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
    detail = Services.objects.get(pk=pk)
    if request.LANGUAGE_CODE == 'en' and not detail.english:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/services/")
    elif request.LANGUAGE_CODE == 'uz' and not detail.uzbek:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/services/")
    elif request.LANGUAGE_CODE == 'ru' and not detail.russian:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/services/")

    # increment views number by one every request
    detail.views += 1
    detail.save()

    return render(request, "service_details.html", {'detail': detail})


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
