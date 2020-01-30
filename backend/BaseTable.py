import boto3
from boto3.dynamodb.conditions import Key, Attr, Not
import os
import time
from uuid import uuid4
from util import BotoException, BotoMetaClass, BotoErrorWrapper
from dotenv import load_dotenv
load_dotenv()


class BaseTable(metaclass=BotoMetaClass):
    ''' wrapper around boto3 ddb table '''

    def __init__(self, tid, key1, key2):
        ''' store relevant info and try to create this table '''
        self.tid = tid
        self.hashkey, self.hktype = key1
        self.rangekey, self.rktype = key2
        self.key_schema = [
            {
                'AttributeName': self.hashkey,
                'KeyType': 'HASH'
            },
            {
                'AttributeName': self.rangekey,
                'KeyType': 'RANGE'
            }
        ]
        self.attr_defn = [
            {
                'AttributeName': self.hashkey,
                'AttributeType': self.hktype
            },
            {
                'AttributeName': self.rangekey,
                'AttributeType': self.rktype
            }
        ]
        try:
            self._create()
        except BotoException as be:
            pass  # this would happend if the table already exists
        except:
            raise

    def key(self, hk, rk):
        ''' make a key for this table '''
        return {self.hashkey: hk, self.rangekey: rk}

    @property
    def res(self):
        ''' load a DDB resource when requested '''
        return boto3.resource(
            'dynamodb',
            aws_access_key_id=os.environ.get('awsaccess'),
            aws_secret_access_key=os.environ.get('awssecret'),
            region_name='us-west-1'
        )

    @property
    def table(self):
        return self.res.Table(self.tid)

    def _create(self, **kw):
        ''' try to create this table '''
        self.res.create_table(
            TableName=self.tid,
            KeySchema=self.key_schema,
            AttributeDefinitions=self.attr_defn,
            ProvisionedThroughput={
                "ReadCapacityUnits": kw.get('RCU', 2),
                "WriteCapacityUnits": kw.get('RCU', 2)
            }
        )
        return 1

    def _put(self, item):
        ''' try to put in an item '''
        if not issubclass(type(item), list):
            item = [item]
        table = self.table
        return [table.put_item(Item=i) for i in item]

    def _query(self, keycondexpr):
        ''' try to query this table '''
        return self.table.query(KeyConditionExpression=keycondexpr)

    def _delete(self, key):
        ''' try to delete something '''
        return self.table.delete_item(Key=key)

    def _scan(self, **kw):
        ''' scan table '''
        return self.table.scan(**kw)

    def _update(self, *args, **kw):
        ''' update an entry in the table '''
        return self.table.update_item(*args, **kw)

    def _format_entry(self, *args, **kw):
        ''' should be overwritten by inheriting classes if nec '''
        pass

    def hashKeyEqLookup(self, hk):
        ''' lookup entry by hash key '''
        return self._query(Key(f"{self.hashkey}").eq(hk))

    def getIfExists(self, hk):
        ''' try to get an entry by hashkey 
        @raise BotoException if no entry 
        @return entry '''
        entry = self.hashKeyEqLookup(hk)
        if entry.get('Count', -1) <= 0:
            raise BotoException(f"{self.hashkey} does not exist")
        return entry.get('Items')

    def raiseIfExists(self, hk):
        ''' try to get an entry by hashkey 
        @raise BotoException if entry exists
        @return entry '''
        entry = self.hashKeyEqLookup(hk)
        if entry.get('Count', -1) > 0:
            raise BotoException(f"{self.hashkey} already exists")
        return entry.get('Items')

    def deleteIfExists(self, hk, rk):
        ''' try to delete an entry 
        @raise BotoException is entry does not exist
        @return 1 '''
        entry = self.getIfExists(hk)
        for e in entry:
            if e[self.rangekey] == rk:
                self._delete(self.key(hk, rk))
                break
        return 1