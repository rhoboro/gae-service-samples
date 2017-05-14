#!/usr/bin/env python
# -*- coding: utf-8 -*-

import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote
from apicollection import api_collection


class ResponseMessage(messages.Message):
    content = messages.StringField(1)


@api_collection.api_class(resource_name='things')
class Thing(remote.Service):
    @endpoints.method(
            message_types.VoidMessage,
            ResponseMessage,
            http_method='GET',
            path='/things'
            )
    def get(self, request):
        return ResponseMessage(content='Hello')

