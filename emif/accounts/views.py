# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import random

try:
    from hashlib import sha1 as sha_constructor
except ImportError:
    from django.utils.hashcompat import sha_constructor

from django.http import HttpResponse
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

import userena.views
from userena.forms import SignupForm, EditProfileForm
from userena.utils import get_user_model
from django_countries.countries import COUNTRIES

from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Profile
from questionnaire.models import Questionnaire

from userena.utils import get_profile_model, get_user_model
from userena.decorators import secure_required
from guardian.decorators import permission_required_or_403
from django.shortcuts import redirect, get_object_or_404

''' adicionámos aqui os imports do demo-django '''
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseServerError)
from django.shortcuts import render_to_response
from django.template import RequestContext

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from django.contrib.auth import authenticate, login

options = (
        (5, '5'),
        (10, '10'),
        (25, '25'),
        (50, '50'),
        (-1, 'All'),
)

class SignupFormExtra(SignupForm):
    """
    A form to add extra fields to the signup form.
    """
    first_name = forms.CharField(label=_('First name'),
                                 max_length=30,
                                 required=True)
    last_name = forms.CharField(label=_('Last name'),
                                max_length=30,
                                required=True)
    country = forms.ChoiceField(COUNTRIES, required=True)

    organization = forms.CharField(label=_('Organization'),
                                   max_length=255,
                                   required=True)

    profiles = forms.ModelMultipleChoiceField(label=_('I am a (select all that apply):'),
                                                required=True,
                                                queryset=Profile.objects.all(),
                                                widget=forms.CheckboxSelectMultiple())


    interests = forms.ModelMultipleChoiceField(label=_('I am interested in (select all that apply):'),
                                                required=True,
                                                queryset=Questionnaire.objects.filter(disable='False'),
                                                widget=forms.CheckboxSelectMultiple())

    paginator = forms.ChoiceField(label=_('Select default value for paginations:'),
                                        choices = options
                                    )

    mail_news = forms.BooleanField(label=_('Receive weekly newsletter e-mail with database updates ?'),
                                    required=False, initial=True
                                    )

    mail_not = forms.BooleanField(label=_('Receive all notifications also over e-mail ?'),
                                    required=False, initial=False
                                    )

    def __init__(self, *args, **kw):
        """
        A bit of hackery to get the added fields at the top of the
        form instead at the end.

        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Delete the username field
        del self.fields['username']

        # Put the new fields at the top

        if Profile.objects.all().count() and Questionnaire.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'email', 'password1', 'password2', 'profiles', 'interests', 'paginator','mail_news', 'mail_not']
        elif Profile.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'email', 'password1', 'password2', 'profiles', 'paginator', 'mail_news', 'mail_not']
        elif Questionnaire.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'email', 'password1', 'password2', 'interests','paginator', 'mail_news', 'mail_not']
        else:
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'email', 'password1', 'password2', 'paginator','mail_news', 'mail_not']

    def save(self):
        """
        Override the save method to save additional fields to the user profile
        and override username with email.

        """
        # Use trimmed email as username
        username = self.cleaned_data['email'][:30]
        try:
            get_user_model().objects.get(username__iexact=username)
        except get_user_model().DoesNotExist:
            pass
        else:  # Fallback to randomly assigned username
            while True:
                username = sha_constructor(str(random.random())).hexdigest()[:5]
                try:
                    get_user_model().objects.get(username__iexact=username)
                except get_user_model().DoesNotExist:
                    break

        self.cleaned_data['username'] = username


        # First save the parent form and get the user.
        new_user = super(SignupFormExtra, self).save()

        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        user_profile = new_user.get_profile()
        user_profile.country = self.cleaned_data['country']
        user_profile.organization = self.cleaned_data['organization']
        try:
            user_profile.paginator = int(self.cleaned_data['paginator'])
        except KeyError:
            user_profile.paginator = 5

        try:
            user_profile.mail_news = self.cleaned_data['mail_news']
        except KeyError:
            user_profile.mail_news = True

        try:
            user_profile.mail_not = self.cleaned_data['mail_not']
        except KeyError:
            user_profile.mail_not = False

        # Add selected profiles
        if (Profile.objects.all().count()):
            selected_profiles = self.cleaned_data['profiles']
            for sp in selected_profiles:
                prof = Profile.objects.get(name=sp)
                user_profile.profiles.add(prof)

        # Add selected interests
        if (Questionnaire.objects.all().count()):
            selected_interests = self.cleaned_data['interests']
            for inter in selected_interests:
                i = Questionnaire.objects.get(name=inter)
                user_profile.interests.add(i)

        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user
class EditProfileFormExtra(EditProfileForm):

    profiles = forms.ModelMultipleChoiceField(label=_('I am a (select all that apply):'),
                                                required=True,
                                                queryset=Profile.objects.all(),
                                                widget=forms.CheckboxSelectMultiple())

    interests = forms.ModelMultipleChoiceField(label=_('I am interested in (select all that apply):'),
                                                required=True,
                                                queryset=Questionnaire.objects.filter(disable='False'),
                                                widget=forms.CheckboxSelectMultiple())

    paginator = forms.ChoiceField(label=_('Select default value for paginations:'),
                                        choices = options
                                    )
    mail_news = forms.BooleanField(label=_('Receive weekly newsletter e-mail with database updates ?'),
                                                required=False,

                                    )

    mail_not = forms.BooleanField(label=_('Receive all notifications also over e-mail ?'),
                                                required=False,
                                    )

    def __init__(self, *args, **kw):
        super(EditProfileFormExtra, self).__init__(*args, **kw)
        del self.fields['mugshot']
        del self.fields['privacy']

        if Profile.objects.all().count() and Questionnaire.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'profiles', 'interests', 'paginator', 'mail_news', 'mail_not']
        elif Profile.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'profiles', 'paginator', 'mail_news', 'mail_not']
        elif Questionnaire.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'interests', 'paginator', 'mail_news', 'mail_not']
        else:
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'paginator']

# Prevent access to edit by not logged in users

@secure_required
def profile_edit(request,
                 edit_profile_form=EditProfileFormExtra,
                 template_name='userena/profile_form.html',
                 success_url=settings.BASE_URL + 'dashboard',
                 extra_context=None, **kwargs):

    if request.user.is_authenticated():
        username = request.user.username
        user = get_object_or_404(get_user_model(),
                                 username__iexact=username)

        profile = user.get_profile()

        user_initial = {'first_name': user.first_name,
                        'last_name': user.last_name}

        form = edit_profile_form(instance=profile, initial=user_initial)

        if request.method == 'POST':
            form = edit_profile_form(request.POST, request.FILES, instance=profile,
                                     initial=user_initial)

            if form.is_valid():
                profile = form.save()
                return redirect(success_url)

        if not extra_context: extra_context = dict()
        extra_context['form'] = form
        extra_context['profile'] = profile
        extra_context['request'] = request
        return userena.views.ExtraContextTemplateView.as_view(template_name=template_name,
            extra_context=extra_context)(request)

    return userena.views.signup(request, **kwargs)

# def profile_edit(request, **kwargs):
#     if request.user.is_authenticated():
#         extra_content = dict()
#         extra_content['request'] = request
#         return userena.views.profile_edit(request, username=request.user.username, extra_content=extra_content, **kwargs)

#     return userena.views.signup(request, **kwargs)

# Prevent access to signup/signin pages by logged in users
def signup(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.BASE_URL)

    return userena.views.signup(request, **kwargs)


def signin(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.BASE_URL)

    return userena.views.signin(request, **kwargs)

#acrescentámos aqui em baixo as funções do views do demo-django
def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)
    return auth


def prepare_django_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    result = {
        'https': 'on' if request.is_secure() else 'off',
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META['SERVER_PORT'],
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy()
    }
    return result


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def sso(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    errors = []
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False

    if 'sso' in req['get_data']:
        print("no sso")
        return HttpResponseRedirect(auth.login())
    elif 'sso2' in req['get_data']:
        print("no sso2")
        return_to = OneLogin_Saml2_Utils.get_self_url(req) + reverse('sso-attrs')
        print return_to
        RR = auth.login(return_to)
        print RR
        return HttpResponseRedirect(auth.login(return_to))
    elif 'slo' in req['get_data']:
        print("no slo")
        name_id = None
        session_index = None
        if 'samlNameId' in request.session:
            name_id = request.session['samlNameId']
        if 'samlSessionIndex' in request.session:
            session_index = request.session['samlSessionIndex']

        return HttpResponseRedirect(auth.logout(name_id=name_id, session_index=session_index))
    elif 'acs' in req['get_data']:
        print("no acs")
        auth.process_response()
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()
        if not errors:
            request.session['samlUserdata'] = auth.get_attributes()
            request.session['samlNameId'] = auth.get_nameid()
            request.session['samlSessionIndex'] = auth.get_session_index()
            if 'RelayState' in req['post_data'] and OneLogin_Saml2_Utils.get_self_url(req) != req['post_data']['RelayState']:
                return HttpResponseRedirect(auth.redirect_to(req['post_data']['RelayState']))
    elif 'sls' in req['get_data']:
        print("no sls")
        dscb = lambda: request.session.flush()
        url = auth.process_slo(delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return HttpResponseRedirect(url)
            else:
                success_slo = True

    print("aquele if no sso")
    print("samlUserdata em request.session?")
    print('samlUserdata' in request.session)
    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()

    return render_to_response('sso/index.html',
                              {'errors': errors,
                               'not_auth_warn': not_auth_warn,
                               'success_slo': success_slo,
                               'attributes': attributes,
                               'paint_logout': paint_logout},
                              context_instance=RequestContext(request))


def attrs(request):
    paint_logout = False
    attributes = False
    req = prepare_django_request(request)
    print("no attrs")
    print("tem samlUserdata no request.session?")
    print ('samlUserdata' in request.session)

    if 'samlUserdata' in request.session:
        paint_logout = True
        print len(request.session['samlUserdata'])
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()
            # get the user email
            for attr in attributes:
                print attr[0]
                if(attr[0] == 'User.email'):
                    user_email = str(attr[1][0])
                    print type(user_email)
                    print(attr[1])
                    print("one login" + user_email)

            try:
                user = authenticate(username=user_email, password=settings.SECRET_KEY, check_password=False)
                login(request, user)
                return_to = OneLogin_Saml2_Utils.get_self_url(req)
            except User.DoesNotExist:
                request.session['email'] = user_email
                return redirect('userena_signup')

    return HttpResponseRedirect(return_to)


            #aceder ao atributo email

    return render_to_response('sso/attrs.html',
                              {'paint_logout': paint_logout,
                               'attributes': attributes},
                              context_instance=RequestContext(request))

def test(request):
    req = prepare_django_request(request)
    print OneLogin_Saml2_Utils.get_self_url(req)
    print("test")
    return_to = OneLogin_Saml2_Utils.get_self_url(req)
    try:
        username = User.objects.get(email__exact="ricardofelgueiras@ua.pt")
        fullname=username.get_full_name()
        print("encontrou user")
    except User.DoesNotExist:
        print("não encontrou user")
        return_to = OneLogin_Saml2_Utils.get_self_url(req) + reverse('userena_signup')
        pass

    return HttpResponseRedirect(return_to)





def metadata(request):
    print("no metadata")
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    saml_settings = auth.get_settings()
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = HttpResponse(content=metadata, content_type='text/xml')
    else:
        resp = HttpResponseServerError(content=', '.join(errors))
    return resp