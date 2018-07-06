# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import date, datetime
from django.db.models import Q
# Create your views here.
def index(request):
	if 'user_id' in request.session:
            return redirect('/user')
	return render(request, 'first_app/test_login.html')

def user(request):
    if not 'user_id' in request.session:
            return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    useritems = Items.objects.filter(Q(added_by=user.username)|Q(item_seekers=user))
    otheritems = Items.objects.exclude(Q(added_by=user.username)|Q(item_seekers=user))
    context = {
        'useritems': useritems,
        'main': user,
        'otheritems': otheritems,
    }
    return render(request, 'first_app/user.html', context)

def register(request):
    errors = []
    for key, val in request.POST.items():
        if len(val) < 3:
            errors.append("{} must be at more than three characters".format(key))

    if len(request.POST['password']) < 8:
    	errors.append("Password must be 8 characters.")

    if request.POST['password'] != request.POST['password_confirmation']:
        errors.append("Password and password confirmation don't match.")

    
    
    if errors:
        for err in errors:
            messages.error(request, err)
        
        return redirect('/')
    
    else:
        try:
            User.objects.get(username=request.POST['username'])
            messages.error(request,"User with that username already exists.")
            return redirect('/')
        except User.DoesNotExist:
        
            hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=request.POST['name'],\
                                username = request.POST['username'], \
                                password = hashpw,\
                                hired = None)
            request.session['user_id'] = user.id

            return redirect('/user')

def login(request):
    try:
        user = User.objects.get(username = request.POST['username'])
        # bcrypt.checkpw(given_password, stored_password)
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/user')
        else:
            messages.error(request, "Username/Password combination FAILED")
            return redirect('/')
    except User.DoesNotExist:
        messages.error(request, "Username does not exist. Please try again")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def add(request):
	if not 'user_id' in request.session:
	    return redirect('/')
	context = {
        'main': User.objects.get(id=request.session['user_id'])
        }
	return render(request, 'first_app/add.html', context)

def additem(request):
	if not 'user_id' in request.session:
            return redirect('/')
	errors = []
	for key, val in request.POST.items():
		if len(val) < 1:
			errors.append("{} cannot be blank!".format(key))  
	if errors:
	    for err in errors:
	        messages.error(request, err)
        
	    return redirect('/add')
    
	else:
		user = User.objects.get(id=request.session['user_id'])    
		Items.objects.create(name = request.POST['item'], added_by = user.username)
		return redirect('/user')

def wishitems(request, id):
	if not 'user_id' in request.session:
            return redirect('/')
	item = Items.objects.get(id=id)
	otherseekers = item.item_seekers.all()
	context = {
		'item': item,
    	'otherseekers': otherseekers
    }
	return render(request, 'first_app/details.html', context)

def join(request, id):
    item = Items.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    item.item_seekers.add(user)
    return redirect('/user')

def delete(request, id):
	user = User.objects.get(id=request.session['user_id'])
	item = Items.objects.get(id=id)

        if item.added_by == user.username:
            # For deleting the user's items
            Items.objects.filter(id=id).delete()
            return redirect('/user')
        else:
            # For removing another user's item
            item.item_seekers.remove(user.id)
	return redirect('/user')