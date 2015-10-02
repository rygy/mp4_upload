from config import aws_key, aws_secret_key

from boto.s3.connection import S3Connection


class FileSeed(object):
    def __init__(self):
        self.conn = S3Connection(aws_key, aws_secret_key)

