# -*- coding: utf-8 -*-
# Copyright (C) 2014 Ricardo F. Gonçalves Ribeiro and Universidade de Aveiro
#
# Authors: Ricardo F. Gonçalves Ribeiro <ribeiro.r@ua.pt>
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

from django.shortcuts import render, render_to_response, redirect

from django.core import serializers
from django.conf import settings
from django.http import *

from .models import *
from django.http import Http404
from django.views.generic import TemplateView

from rest_framework import permissions
from rest_framework import renderers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.permissions import AllowAny, IsAuthenticated

from django_datatables.models import *

class Index(TemplateView):
    template_name = "communities.html"
    def get(self, request):
        return render(request, self.template_name, {'request': request, 'dashboard': True, 'breadcrumb': True})


class List(TemplateView):
    template_name = "communities_list.html"
    def get(self, request):
        return render(request, self.template_name, {'request': request, 'breadcrumb': True})

class ListFilters(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kw):

        if request.user.is_authenticated():
            dictionary = {
                "draw": 1,
                "recordsTotal": 1,
                "recordsFiltered": 1,
                "data": [
                    {
                        "logo": "http://127.0.0.1:8000/static/img/emif_logo_trans.png",
                        "name": "Emif Catalogue",
                        "date_created": "12-12-1212 12:12:12",
                        "members": 190,
                        "manage": False
                    }
                ]
            }

            table = DataTable.fromPOST(request.POST)

            dictionary['draw'] = table.draw

            response = Response(dictionary, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response
