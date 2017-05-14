from google.appengine.ext import ndb
import json


class Article(ndb.Model):
    author = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    body = ndb.TextProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def _create(cls, req):
        dic = json.load(req.stream) if req.content_length else {}
        author = dic.get('author')
        title = dic.get('title')
        body = dic.get('body')
        if author and title and body:
            return Article(author=author, body=body, title=title)
        else:
            return None

    create = _create

    @classmethod
    def _fetch(cls, req):
        key_str = req.get_param('key') or ''
        if len(key_str) > 0:
            try:
                key = ndb.Key(urlsafe=key_str)
                if key:
                    article = key.get()
                    articles = [article]
                else:
                    articles = []
            except Exception:
                articles = []
        else:
            articles = Article.query()
        return articles

    fetch = _fetch
