from __future__ import print_function
from django.template import Context, loader, RequestContext
from app.models import Contacts
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

#ModelForms
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.utils import timezone
from django.views.decorators import csrf
from django.urls import reverse , resolve
from django.core.mail import send_mail

from .forms import ContactForm, LookupForm, CancelForm

#Recycling logic
from .recycle import parse_address, confirm_subscription, cancel_subscription, get_initial_message, insert_contact, get_zones, insert_initial_message, select_initial_message

#Hash value for obfuscating primary key.  stackoverflow.com/questions/10559935/django-how-do-i-hash-a-url-from-the-database-objects-primary-key
from mysite.passwords import OBFUSCATE

#Logo image
logo_image="recyclobuddy_logo.jpg"

# Create your views here.

#See pydanny.com/core-concepts-django-modelforms.html, but note several errors in the example code.
def index(request):
    message = ""
    if request.method == "POST":
        form = LookupForm(request.POST)

        if form.is_valid():

            #Capture fields from the form
            municipality=form.cleaned_data['municipality']
            address=form.cleaned_data['address']
            zip=form.cleaned_data['zip']

            #Parse address to put into standard form.  Check for error
            error_code, parsed_address = parse_address(address, municipality)


            if error_code == 1:
                #If error_code==1, failed to find street identifier
                message = "Didn't work. Please check municipality and omit apartment or suite from address."
                subscribe_URL=""

            else:
                #Looks good, go ahead with the process

                #Look up zone information and return a zone dictionary giving zone and day for recycling, trash and yard waste
                try: 
                    zone_dict = get_zones(municipality, parsed_address, zip)
                    server_failed=False
                except Exception:
                    zone_dict = False
                    server_failed=True
                    raise

                if zone_dict:
                        #Do lookup from schedules table and get message
                        messages=get_initial_message(municipality, zone_dict)

                        #Copy result into contacts table
                        primary_key=insert_contact(municipality, parsed_address, zip, zone_dict)

                        #Copy message into initial_messages table
                        insert_initial_message(primary_key, messages)

                        #Obfuscate the primary key
                        masked_key = primary_key ^ OBFUSCATE

                        #Create URL for subscription with primary key
                        subscribe_URL="subscribe_" + str(masked_key)

                        #Redirect to subscription page
                        return HttpResponseRedirect(subscribe_URL)

                else:
                        #Failed.  Could be the address wasn't good, (server_failed is False), or that server can't be reached. 
                        if server_failed==False:
                            message = "Didn't work. City couldn't locate that address. Is it correct?"
                        else:
                            message = "Can't reach city server. Email recyclobuddy@recyclobuddy.com for help."
                            
                        subscribe_URL=""
                        form=LookupForm(request.POST)

            #Failed to get address in usable form or failed in zone look up

            c = {
                    'app_template': 'app/basic_template.html',
                    'logo_image' : logo_image,
                    'message': message,
                    'subscribe_URL': subscribe_URL,
                    'form' : form
            }

            return render (request, "app/index.html", c )

        else:
            c = {
                    'app_template': 'app/basic_template.html',
                    'logo_image' : logo_image,
                    'message': 'Hit a snag on street address. Leave off any apt or suite info',
                    'form' : form
            }

            return render (request, "app/index.html", c ) 
    else:
        form = LookupForm(initial={'municipality': 'LOWER_MERION'})

    c = {
        'app_template': 'app/basic_template.html',
        'logo_image' : logo_image,
        'form': form,
    }

    return render (request, "app/index.html", c ) 

#@login_required
def subscribe(request, masked_key):
    #undo obfuscation
    primary_key = int(masked_key) ^ OBFUSCATE

    cat = get_object_or_404(Contacts, index_key=primary_key)

    #If this request has already been submitted, show the acknowledge page to avoid exposing private data.
    if cat.request==True:
        c = {
            'app_template': 'app/basic_template.html',
            'logo_image' : logo_image,
            }
        #Send URL acknowledging request
        return render (request, "app/acknowledge.html", c )

    if request.method == "POST":
        #Using the instance here allows an update.  docs.djangoproject.com/en/1.1/topics/forms/modelforms/#the-dave-method
        form = ContactForm(request.POST, instance=cat)

        if form.is_valid():
            model_instance = form.save()
            primary_key = model_instance.pk

            #Create message for confirmation
            confirmation_message=confirm_subscription(
                masked_key, 
                model_instance.first_name,
                model_instance.last_name,
                model_instance.alert_day,
                model_instance.alert_time,
                model_instance.email_alert,
                model_instance.sms_alert,
            )
            
            #Update Contacts to reflect confirmation request
            c=Contacts.objects.get(pk=primary_key)
            c.request=True
            c.save()

            #Send mail message add try catch ???
            try:
                    send_mail('Confirmation request', confirmation_message, 'recyclobuddy@recyclobuddy.com', [model_instance.email], fail_silently=False)
            except Exception:
                print ("Failed to send confirmation email\n")


                c = {
                'app_template': 'app/basic_template.html',
                'logo_image' : logo_image,
                }
            #Send URL acknowledging request
                return render (request, "app/acknowledge.html", c )

    else:
            
        form=ContactForm(instance = cat)
    
    #You are here either because ir's presenting the form before data is added, or the data isn't valid.
        
    #Get message information
    messages=select_initial_message(primary_key)


    c = {
        'app_template': 'app/basic_template.html',
        'logo_image' : logo_image,
        'message_1': messages[0],
        'message_2': messages[1],
        'message_3': messages[2],
        'form': form,
    }

    return render(request, "app/subscription.html", c ) 

#@login_required
def confirm(request, masked_key):
    #undo obfuscation
    primary_key = int(masked_key) ^ OBFUSCATE

    #Check if there is a valid object for this primary key
    cat = get_object_or_404(Contacts, index_key=primary_key)

    #Do validation:  Does object exist and is request outstanding?
    c=Contacts.objects.get(pk=primary_key)
    if c and c.request==True:
            valid=True
    else:
        valid=False

    #If validation passed, then send confirmation message
    if valid == True:
        #Update Contacts to reflect subscription
        c.subscribe=True
        c.save()


        #Send okay message

        c = {
            'app_template': 'app/basic_template.html',
            'logo_image' : logo_image,
        }
        return render(request, "app/confirm.html", c )

    else:
        #Failed, so send back to beginning.
        form=LookupForm()

    c = {
        'app_template': 'app/basic_template.html',
        'logo_image' : logo_image,
        'form': form,
    }

    return render(request, "app/try_again.html", c ) 

#@login_required
def cancel(request):
    if request.method == "POST":
        form = CancelForm(request.POST)
        if form.is_valid():

            #Capture fields from the form
            email=form.cleaned_data['email']
            mobile=form.cleaned_data['mobile']

            #Check if email and mobile combination in database
            success=cancel_subscription(email, mobile)

            if success==True:
                    #Cancellation worked.
                        c = {
                    'app_template': 'app/basic_template.html',
                    'logo_image' : logo_image,
                        }
                        return render(request, "app/gone.html", c )

            else:
                #Cancellation failed
                form = CancelForm()
                message = "We couldn't find that combination of email address and mobile number. Please try again."

                c = {
                        'app_template': 'app/basic_template.html',
                        'logo_image' : logo_image,
                        'message': message,
                        'form': form,
                    }

                return render(request, "app/cancel.html", c )

    else:
        form = CancelForm()
        message = "Sorry to see you go! Please enter email and mobile number to discontinue alerts."
        
        c = {
                'app_template': 'app/basic_template.html',
                'logo_image' : logo_image,
                'message': message,
                'form': form,
            }

        return render(request, "app/cancel.html", c )

def about(request):
    c = {
        'app_template': 'app/basic_template.html',
        'logo_image' : logo_image,
    }

    return render(request, "app/about.html", c )

def faq(request):
    c = {
        'app_template': 'app/basic_template.html',
        'logo_image' : logo_image,
    }

    return render(request, "app/faq.html", c )

def terms(request):
    c = {
        'app_template': 'app/basic_template.html',
        'logo_image' : logo_image,
    }

    return render(request, "app/terms.html", c )

def trash_talk(request):
    c = {
        'app_template': 'app/basic_template.html',
        'logo_image' : logo_image,
    }

    return render(request, "app/trash-talk.html", c )

def share(request):
    c = {
        'app_template': 'app/basic_template.html',
        'logo_image' : logo_image,
    }

    return render(request, "app/share.html", c )

#@login_required
def test(request):
    c = {
        'app_template': 'app/basic_template.html',
        'logo_image' : logo_image,
    }

    return render(request, "app/repairs.html", c )

#@login_required
def root_index(request):
    return HttpResponseRedirect('./app/')

@login_required
def success(request):
    return HttpResponseRedirect('../app/index')

#@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('../')
