# -*- coding: utf-8 -*-

# Copyright (C) 2014 Tiago Miguel V.F. Lourenço and Universidade de Aveiro
#
# Authors: Tiago Miguel V.F. Lourenço <tiago.vf.lourenco@ua.pt>
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

from django.shortcuts import render, render_to_response

from django.core import serializers

from django.conf import settings

from django.http import *

from django.template import RequestContext

from searchengine.search_indexes import CoreEngine

from questionnaire.models import *
from questionnaire.parsers import *
from questionnaire.views import *
from questionnaire.models import *

from fingerprint.services import *
from fingerprint.models import *
from fingerprint.tasks import anotateshowonresults

from emif.views import createqsets, createqset, get_api_info, getPermissions, attachPermissions, merge_highlight_results

import random
import datetime
import time

def teste(request, template_name='teste.html'):
    return render(request, template_name)


def get_databases_from_solr(request, query="*:*"):

    (list_databases, hits) = get_databases_from_solr_v2(request, query=query);

    return list_databases

def get_databases_from_solr_v2(request, query="*:*", sort="", rows=100, start=0, fl='',post_process=None):
    c = CoreEngine()
    results = c.search_fingerprint(query, sort=sort, rows=rows, start=start, fl=fl)
    
    list_databases = get_databases_process_results(results)

    if post_process:
        list_databases = post_process(results, list_databases)
    
    return (list_databases,results.hits)

def get_databases_process_results(results):
    print "Solr"
    list_databases = []
    questionnaires_ids = {}
    qqs = Questionnaire.objects.all()
    for q in qqs:
        questionnaires_ids[q.slug] = (q.pk, q.name)

    for r in results:
        try:
            database_aux = Database()
            
            database_aux.id = r['id']

            if (not r.has_key('created_t')):
                database_aux.date = ''
            else:

                try:
                    database_aux.date = convert_date(r['created_t'])
                except:
                    database_aux.date = ''


            if (not r.has_key('date_last_modification_t')):
                database_aux.date_modification = convert_date(r['created_t'])
            else:

                try:
                    database_aux.date_modification = convert_date(r['date_last_modification_t'])
                except:
                    database_aux.date_modification = convert_date(r['created_t'])

            if (not r.has_key('database_name_t')):
                database_aux.name = '(Unnamed)'
            else:
                database_aux.name = r['database_name_t']

            database_aux.localtion = ''

            if(r.has_key('city_t')):
                database_aux.location = r['city_t']
            if (r.has_key('location_t')):
                database_aux.location = r['location_t']
            if (r.has_key('PI:_Address_t')):
                database_aux.location = r['PI:_Address_t']

            if (not r.has_key('institution_name_t')):
                database_aux.institution = ''
            else:
                database_aux.institution = r['institution_name_t']

            if (not r.has_key('contact_administrative_t')):
                database_aux.email_contact = ''
            else:
                database_aux.email_contact = r['contact_administrative_t']

            if (not r.has_key('number_active_patients_jan2012_t')):
                database_aux.number_patients = ''
            else:
                database_aux.number_patients = r['number_active_patients_jan2012_t']

            if (not r.has_key('date_last_modification_t')):
                database_aux.last_activity = ''
            else:
                database_aux.last_activity = r['date_last_modification_t']                
                
            if (not r.has_key('upload-image_t')):
                database_aux.logo = 'nopic.gif'
            else:
                database_aux.logo = r['upload-image_t']

            (ttype, type_name) = questionnaires_ids[r['type_t']]
            database_aux.ttype = ttype
            database_aux.type_name = type_name
            database_aux = __get_scientific_contact(database_aux, r, database_aux.type_name)
            #import pdb
            #pdb.set_trace()
            list_databases.append(database_aux)
        except Exception, e:
            print e
            pass

    return list_databases


def index(request, template_name='statistics1.html'):
    #return HttpResponse("Hello, world. You're at the poll index.")
    query = None
    isAdvanced = False
    if(request.session.get('isAdvanced') == True): 
        query = request.session.get('query')
        if query == None:
            query = "*:*"

        isAdvanced = True
    else:
        if(request.session.get('query') != None):
            query = "'"+re.sub("['\"']","\\'",request.session.get('query'))+"'"  
            query = "text_t:"+query

        else:
            query = "*:*"

    #print "query@" + query
    list_databases = get_databases_from_solr(request, query)
    print isAdvanced

    return render(request, template_name, {'request': request, 'search_old': request.session.get('query',''), 
                                           'breadcrumb': True, 'isAdvanced': isAdvanced})


def database_statistics_view(request, questionnaire_id, template_name='statistics_qs.html'):
    return database_statistics_view_dl(request, questionnaire_id, "1", template_name)

def database_statistics_view_dl(request, questionnaire_id, sort_id, template_name='statistics_qs.html'):
    return render(request, template_name, {'request': request,'breadcrumb': True});