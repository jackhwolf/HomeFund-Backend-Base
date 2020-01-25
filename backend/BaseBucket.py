import boto3
import os
import sys
from uuid import uuid4
import time
from util import BotoMetaClass
from dotenv import load_dotenv
load_dotenv()


class BaseBucket(metaclass=BotoMetaClass):
    ''' class to manage S3 '''

    def __init__(self, name):
        self.bucket_name = name
        self.loc = "us-west-1"
  
    @property
    def cli(self):
        ''' get an S3 client '''
        return boto3.client(
            's3',
            aws_access_key_id=os.environ.get('awsaccess'),
            aws_secret_access_key=os.environ.get('awssecret'),
            region_name='us-west-1'
        )

    @property
    def res(self):
        ''' get an S3 resource '''
        return boto3.resource(
            's3',
            aws_access_key_id=os.environ.get('awsaccess'),
            aws_secret_access_key=os.environ.get('awssecret'),
            region_name='us-west-1'
        )

    @property
    def bucket(self):
        ''' get this bucket '''
        return self.res.Bucket(self.bucket_name)

    def _create(self, **kw):
        ''' try to create this bucket 
        @kw: kwargs to pass to S3 create '''
        resp = self.cli.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration={'LocationConstraint': self.loc}, **kw)
        return resp

    def _upload(self, key, fileObj, **kw):
        ''' try to upload a file to this bucket 
        @params:
            key:     str, S3 key for fileObj
            fileObj: binary file contents to upload '''
        resp = self.bucket.upload_fileobj(fileObj, key)
        return resp

    def _get(self, key):
        ''' try to get an object from this bucket. for our purposes, we do not need this
        because we will give paths to objects instead of objects themselves. '''
        pass

    # TODO
    def _list(self):
        ''' list the contents of a bucket '''
        pass
    def _delete_obj(self, key):
        ''' try to delete an object from this bucket
        @params:
            key: str, key to object in S3 '''
        resp = self.res.Object(self.bucket_name, key)
        return resp

    def _delete_bucket(self):
        ''' try to delete this bucket '''
        _ = [key.delete() for key in self.bucket.objects.all()]
        resp = self.bucket.delete()
        return resp

