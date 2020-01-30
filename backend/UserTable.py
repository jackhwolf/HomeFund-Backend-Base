from BaseTable import BaseTable
from time import time
from util import BotoException

'''
this file defines our user database which extends the BaseTable. This table is used for all
user operations like adding new users, deleting users, and updating user data
'''

class UserTable(BaseTable):

    def __init__(self):
        BaseTable.__init__(
            self, 'users-HomeFund', ('username', 'S'), ('password', 'S'))
        self.user_types = {    # keep map to types of users
            1: 'typeA',
            2: 'typeB'
        }

    def _format_entry(self, uname, pword, realname, contact, banking, usertype):
        ''' create a standard new entry for a user with given username and password

        brief explanation of keys in entry:
            username:     the username that the user will go by on the app. their user ID
            password:     the users password
            realname:     the users real name, whats on their issued ID
            contactInfo:  the users contact info. a dict with either 'phone' or 'email'
            bankingInfo:  the banking/payment info we have for the user
            userType:     describes what type of user this is
            groupIDs:     IDs of groups user is active in
            taskIDs:      IDs of tasks assigned to user
            score:        HomeFund score of user
            stats:        users aggregated stats 
            createdAt:    epoch time of signup

        @params:
            uname:    str,  username of new user
            pword:    str,  password of new user
            realname: str,  real name of new user
            contact:  dict, contact info of new user. maps to 'phone' and/or 'email'
            banking:  ???,  banking information of new user
            usertype: int,  key to self.user_types
        @return dict, new entry for user
        '''
        return {
            'username': uname, 'password': pword,
            'realname': realname, 'contactInfo': contact,
            'bankingInfo': banking, 'userType': self.user_types[usertype],
            'groupIDs': [], 'taskIDs': [], 'score': 0, 'stats': [],
            'createdAt': int(time() * 1000)
        }

    def putBadUser(self):
        ''' use this to check that exceptions are being properly thrown '''
        return self._put({'bad': 'stuff', 'wont': 'work'})
