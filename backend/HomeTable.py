from BaseTable import BaseTable
from time import time

'''
this file defines the database we use to work with the Homes. a Home is a collection
of users that assign/complete tasks. a Home needs to be able to add/delete users, 
submit/complete tasks, and store notes about the house
'''

class HomeTable(BaseTable):

    def __init__(self):
        BaseTable.__init__(self, 'homes-HomeFund', ('homeID', 'S'), ('createdAt', 'N'))

    def _format_entry(self, homeid):
        ''' create standard entries for new homes
        
        brief description of keys in entry:
            homeID:    unique ID of home
            createdAt: time this home was created
            users:     list of users IDs in house
            tasks:     list of active task IDs
            balance:   account balance of home fund
            feedback:  feedback for this house

        @params:
            homeid: str, unique ID of home
        @return dict, new entry
        '''
        return {
            'homeID': homeid, 'createdAt': int(time() * 1000),
            'users': [], 'tasks': [], 'balance': 0, 'feedback': []
        }
