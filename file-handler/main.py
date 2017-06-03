#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import app_identity
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers as bh

BUCKET_NAME = app_identity.get_default_gcs_bucket_name()
BASE_PATH = '/file-handler'
CALLBACK_URL = BASE_PATH + '/uploaded'
BASE_UPLOAD_URL = BASE_PATH + '/upload'
BASE_DOWNLOAD_URL = BASE_PATH + '/download/'

class GSFile(ndb.Model):
    filename = ndb.StringProperty()
    size = ndb.IntegerProperty()
    content_type = ndb.StringProperty()
    blob_key = ndb.StringProperty()
    creation = ndb.DateTimeProperty()

    @classmethod
    def create(cls, blob_info):
        entity = cls(
                filename=blob_info.filename,
                size=blob_info.size,
                content_type=blob_info.content_type,
                creation=blob_info.creation,
                blob_key=str(blob_info.key())
                )
        entity.put()

    @classmethod
    def fetch_by_name(cls, filename):
        return cls.query().filter(cls.filename == filename).order(-cls.creation).get()


class UploadHander(webapp2.RequestHandler):
    def get(self):
        url = blobstore.create_upload_url(CALLBACK_URL, gs_bucket_name=BUCKET_NAME + '/files')
        self.response.write(url)


class UploadComplitionHander(bh.BlobstoreUploadHandler):
    def post(self):
        for blob in self.get_uploads('file'):
            GSFile.create(blob)
        self.response.status = 204


class DownloadHandler(bh.BlobstoreDownloadHandler):
    def get(self, filename):
        gs_file = GSFile.fetch_by_name(filename)
        if gs_file:
            blob_info = blobstore.BlobInfo.get(gs_file.blob_key)
            self.send_blob(blob_info, save_as=True)
        else:
            self.response.status = 404


app = webapp2.WSGIApplication([
    (BASE_UPLOAD_URL, UploadHander),
    (CALLBACK_URL, UploadComplitionHander),
    (BASE_DOWNLOAD_URL + r'(.*)', DownloadHandler)
    ], debug=True)

