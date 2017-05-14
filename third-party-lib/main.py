#!/usr/bin/env python
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

import falcon
import json
from middleware import CORSMiddleware
from model.article import Article


class ArticleResource(object):
    def on_get(self, req, resp):
        articles = Article.fetch(req)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'articles': [
            {'key': article.key.urlsafe(), 'author': article.author, 'title': article.title, 'body': article.body} for article in
            articles]})

    def on_post(self, req, resp):
        article = Article.create(req)
        if article:
            key = article.put()
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({'key': key.urlsafe()})
        else:
            resp.status = falcon.HTTP_400
            resp.body = "400 Bad Request."

    def on_options(self, req, resp):
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        articles = Article.fetch(req)
        if len(articles) != 1:
            resp.status = falcon.HTTP_400
            resp.body = '400 Bad Request'
        else:
            article = articles[0]
            article.key.delete()
            resp.status = falcon.HTTP_204


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
articleResource = ArticleResource()

# article will handle all requests to the '/articles' URL path
app.add_route('/third-party-lib/articles', articleResource)
