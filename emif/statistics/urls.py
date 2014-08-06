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

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   
    # Reeditar
    #url(r'^dbDetailed/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)$', 'emif.views.database_detailed_view'),
    url(r'^index$', 'statistics.views.index'),
    url(r'^teste$', 'statistics.views.teste'),
    url(r'^dbStatistics/(?P<questionnaire_id>[0-9]+)/$', 'statistics.views.database_statistics_view'),
    url(r'^dbStatistics/(?P<questionnaire_id>[0-9]+)/(?P<sort_id>[0-9]+)/$', 'statistics.views.database_statistics_view_dl'),
)