# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain

from django.shortcuts import render, redirect
import django.contrib.postgres.search as search
from django.http import HttpResponse
from taborniki.models import Oseba
from django.db.models import Q
from .forms import NameForm, DodajClan, Search


def search_results(request, isci):
    # poiščemo po imenu
    clani1 = Oseba.objects.filter(ime__contains=isci)
    # poiščemo po priimku
    clani2 = Oseba.objects.filter(priimek__contains=isci)
    # združimo in odstranimo duplikate
    clani = list(set(list(chain(clani1, clani2))))
    return render(request, 'taborniki/tabele.html', {'clani':clani})


def index(request):
    if request.method == 'GET':
        form = Search(request.GET)
        if form.is_valid():
            data = form.cleaned_data['q']
            return redirect('/taborniki/search/%s' % data)
    form = Search()
    return render(request,'taborniki/base.html',  {'form': form} )

def login(request):
    return render(request,'taborniki/login.html' )

def profil(request):
    return render(request,'taborniki/search_results.html')

def clani(request):
    clani = Oseba.objects.all()
    output = ', '.join([p.__str__() for p in clani])
    return HttpResponse(output)

def get_name(request, clan_id):
    clan = Oseba.objects.get(id = clan_id)
    return render(request, 'taborniki/search_results.html', {'clan': clan})



def dodajClan(request):
    if request.method == 'POST':
        form = DodajClan(request.POST)
        print(form)
        print(form.cleaned_data)
        print(form.is_valid())
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            clan = Oseba.objects.create(ime = data['ime'],priimek=data['priimek'], naslov=data['naslov'],
                                        telefon=data['telefon'] , email=data['email'] , rojstvo=data['rojstvo']  )
            clan.save()

            return redirect('/taborniki/profil/%s' % clan.id )


    # if a GET (or any other method) we'll create a blank form
    else:
        form = DodajClan()

    return render(request, 'taborniki/dodajClan.html', {'form': form})