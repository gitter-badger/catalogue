
# -*- coding: utf-8 -*-

# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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
from bson.objectid import ObjectId 
from emif.settings import jerboa_collection, jerboa_aggregation_collection
from pymongo.errors import OperationFailure
import copy
import json 

from population_characteristics.conf_aggregations import *


from searchengine.search_indexes import * 
import itertools
from sets import Set

"""
This class do the aggregations from data comming from Jerboa 
Marius and Peter from Erasmus MC has developed an R script to perform this task
This class will a translation of their script 
This will be a task asynchonous executed through the celery (background tasks)
to scale the solution
"""

class AggregationPopulationCharacteristics(object):
    """
    @param values data parsed comming from Jerboa
    """
    def __init__(self, values, fingerprint_id, revision=None):
        self.values = values 
        #print self.values 
        _ca = ConfAggregations()
        #print _ca
        # Get the aggregations 
        self.confs = _ca.get_main_settings()
        self.fingerprint_id = fingerprint_id 

        # Doing a pre-processing to become the aggregation task easier
        self.var_pre_process_dict = {}
        print self.confs
        for c in self.confs:
            print c.var

            if c.var in self.var_pre_process_dict:
                self.var_pre_process_dict[c.var].append(c)
            else:
                self.var_pre_process_dict[c.var] = [c]
        print "var_pre_process_dict"
        print self.var_pre_process_dict

        self.index_new_values = {}

    """ Get the slug value (which going to fingerprint take that value)
    """
    def __get_slug_values(self, slug_name):
        solr = CoreEngine()
        # Get the results
        results = solr.search_fingerprint("id:" + self.fingerprint_id)
        for r in results:
            return [r[slug_name]]

    """ Get the value from 
    """
    def __get_tsv_values(self, name, var):
        
        # Go to mongodb and ask for the values or ask directly in the values 
        values = Set([])
        
        for e in self.values:
            
            if e['values']['Var'] == var:
                values.add(e['values'][name])
            #else:
                #print e['values'][name]
                #print e['values']['Var']
        return list(values)

    def __get_values(self, agregation_field, aggregation):
        # TODO: this process can be cached!
        # Optimization++
        if agregation_field.ttype =="slug":
            agregation_field.values = self.__get_slug_values(agregation_field.name)
            return agregation_field.values
        elif agregation_field.ttype =="tsv":
            agregation_field.values = self.__get_tsv_values(agregation_field.value, aggregation.var)
            return agregation_field.values


    # Agregate the entry 
    def __aggregate_entry(self, entry):
        try:
            #print "check if it have"
            #print entry['values']['Var']
            if entry['values']['Var'] in self.var_pre_process_dict: 
                # It is the type of we want to aggregate, so we need to do some calculations 
                
                for aggregation in self.var_pre_process_dict[entry['values']['Var']]:
                    # Get Aggregation Field
                    #print "check aggregations now "
                    arr_values = []
                    for af in aggregation.aggregation_fields:
                        if (af.values==None):
                            value = self.__get_values(af, aggregation)    
                            if value == None:
                                print "fuck"
                                print af.key
                                print af.value
                                print af.name
                                print aggregation.var
                            af.values = value 

                            arr_values.append(af.values)
                    #print "Processing: " + entry['values']['Var']
                    #print "arr_values: " +str(arr_values)
                    if arr_values!=[]:
                        for combination in itertools.product(*arr_values, repeat=1):
                            print combination
                            

                            if combination in self.index_new_values:
                                print "has value"
                                _entry = self.index_new_values[combination]
                                # TODO: Check the operation 
                                # For now, only sums
                                _entry['values'][aggregation.field_to_compute] = _entry['values'][aggregation.field_to_compute]  +  entry['values'][aggregation.field_to_compute]
                            else:
                                print "not has value"
                                _entry = copy.deepcopy(entry)
                                _entry['values']['Name1'] = ''
                                _entry['values']['Name2'] = ''
                                _entry['values']['Value1'] = ''
                                _entry['values']['Value2'] = ''
                                #entry['values'] = {}
                                _entry['values'][aggregation.field_to_compute] = _entry['values'][aggregation.field_to_compute]
                                i = 0 
                                for af in aggregation.aggregation_fields:
                                    #print combination
                                    #print i
                                    if af.ttype == "slug":
                                        _entry['values'][af.value] = combination[i]
                                        _entry['values'][af.key] = af.key 
                                    else:
                                        #print "af.value" + af.value +  combination[i]
                                        #print "af.value" + af.value +  _entry['values'][af.value] 
                                        _entry['values'][af.value] = str(combination[i])
                                        if (af.key!=None):
                                            _entry['values'][af.key] = entry['values'][af.key]

                                    i = i + 1
                                #print "to store"
                                #print _entry 
                                #print id(_entry )
                                #print self.index_new_values
                                self.index_new_values[combination] = _entry
                                #print self.index_new_values
                                self.new_values.append(_entry)
                                
                    #print "end combination"
            #else:
                #print "no"
        


        except:
            print "Exception!!!!!!!"
            import traceback
            traceback.print_exc()


    # Loads the previous aggregations if required 
    def __load_previous_values_from_aggregation(self):
        return []

    """ Execute the aggregation""" 
    def run(self):
        
        # Load the previous aggregations, if required 
        self.new_values = self.__load_previous_values_from_aggregation()

        # Run all the values and aggregate them 
        for entry in self.values:
            #print "entry"
            #print entry
            # Now Let's execute the aggregator task
            #print "self.__aggregate_entry(entry)"
            self.__aggregate_entry(entry)
        
        
        
        try:
            #Create MONGO record
            print "Create MONGO record"
            for doc in self.new_values: 
                doc['_id'] = ObjectId() 
                jerboa_aggregation_collection.insert(doc)
            
            print "Sucess "
        except OperationFailure as e:
            print "Failure"
            print e
            import traceback
            traceback.print_exc()
        print "finishing staff"
        return self.new_values 
        
