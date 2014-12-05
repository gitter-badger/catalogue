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


from fingerprint.models import *
from django.db.models import Avg, Count, Sum, Min, Max



class FingerprintSchemaStats(object):


    def __init__(self, fingerprint_schema):

        """@param fingerprint_schema Receive Questionnarie
        """

        self.fingerprint_schema = fingerprint_schema


    def totalDatabases(self):

        q = Fingerprint.getActiveFingerprints(self.fingerprint_schema)
        return q.count()


    def totalDatabaseOwners(self):
        q = Fingerprint.getActiveFingerprints(self.fingerprint_schema)
        return q.count()


    def totalDatabaseShared(self):
        return Fingerprint.objects.filter(\
            questionnaire=self.fingerprint_schema).annotate(\
            num_shared=Count('shared')).aggregate(Sum('num_shared'))

    def maxDatabaseShared(self):
        return Fingerprint.objects.filter(\
            questionnaire=self.fingerprint_schema).annotate(\
            num_shared=Count('shared')).aggregate(Sum('num_shared'))


    def maxDatabaseShared(self):
        return Fingerprint.objects.filter(\
            questionnaire=self.fingerprint_schema).annotate(\
            num_shared=Count('shared')).aggregate(Sum('num_shared'))



    def totalFilledQuestions(self):
        return Answer.objects.filter(\
            fingerprint_id__questionnaire=self.fingerprint_schema).annotate(\
            num_questions=Count('questions')).aggregate(Sum('num_questions'))


    def maxFilledFingerprints(self):
        return Fingerprint.objects.filter(\
            questionnaire=self.fingerprint_schema).aggregate(Max('fill'))


    def minFilledFingerprints(self):
        return Fingerprint.objects.filter(\
            questionnaire=self.fingerprint_schema).aggregate(Min('fill'))


    def avgFilledFingerprints(self):
        return Fingerprint.objects.filter(\
            questionnaire=self.fingerprint_schema).aggregate(Avg('fill'))


    def totalDatabaseUsers(self):
        return self.totalDatabaseShared() + self.totalDatabaseOwners()


    def totalInterested(self):
        return EmifProfile.objects.filter(interests__contains=self.fingerprint_schema).count()
        EmifProfile.objects.filter(interests=qq).count()


class FingerprintStats(object):

    def __init__(self, fingerprint):
        pass

    def questions(self):
        pass


