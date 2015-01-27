from django.db import models

from querystring_parser import parser

def get_bool(value):
    return value in ('True', 'true')

class DataTableSearch:
    def __init__(self, value, regex):
        self.value = value
        self.regex = get_bool(regex)

    @staticmethod
    def fromDICT(dict):
        return DataTableSearch(dict['value'], dict['regex'])

    def __repr__(self):
        return "<DataTableSearch: %s>" % (self.__dict__)

class DataTableOrder:
    def __init__(self, column, dir):
        self.column = int(column)
        self.dir = dir

    @staticmethod
    def fromDICT(dict):
        array = []

        for key in dict:
            array.append(DataTableOrder(dict[key]['column'], dict[key]['dir']))

        return array

    def __repr__(self):
        return "<DataTableOrder: %s>" % (self.__dict__)

class DataTableColumn:
    def __init__(self, data, search, searchable, orderable, name):
        self.data = data
        self.search = search
        self.searchable =  get_bool(searchable)
        self.orderable =  get_bool(orderable)
        self.name = name

    @staticmethod
    def fromDICT(dict):
        array = []

        for key in dict:
            this_value = dict[key]
            array.append(
                DataTableColumn(
                    this_value['data'],
                    DataTableSearch.fromDICT(this_value['search']),
                    this_value['searchable'],
                    this_value['orderable'],
                    this_value['name']
                )
            )

        return array

    def __repr__(self):
        return "<DataTableColumn: %s>" % (self.__dict__)

class DataTable:
    def __init__(self):
        self.columns = []
        self.search = []
        self.order = []
        self.start = 0
        self.draw = 1
        self.length = 10

    def __repr__(self):
        return "<DataTable: %s" % (self.__dict__)

    @staticmethod
    def fromPOST(post):
        post_dict = parser.parse(post.urlencode())

        table = DataTable()

        table.draw = post_dict['draw']
        table.start = post_dict['start']
        table.length = post_dict['length']
        table.search = DataTableSearch.fromDICT(post_dict['search'])
        table.order = DataTableOrder.fromDICT(post_dict['order'])
        table.columns = DataTableColumn.fromDICT(post_dict['columns'])

        return table
