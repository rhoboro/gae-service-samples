#!/usr/bin/env python
# -*- coding: utf-8 -*-

import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote
from apicollection import api_collection


class RequestMessage(messages.Message):
    content = messages.StringField(1)


class ResponseMessage(messages.Message):
    content = messages.StringField(1)
    entity_id = messages.IntegerField(2)
    query_param = messages.StringField(3)

RESOURCE_CONTAINER = endpoints.ResourceContainer(
        RequestMessage,
        entity_id=messages.IntegerField(2),
        query_param=messages.StringField(3))

@api_collection.api_class(resource_name='resources')
class Resource(remote.Service):

    @endpoints.method(
            RequestMessage,
            ResponseMessage,
            path='/resources'
            )
    def post(self, request):
        return ResponseMessage(content=request.content)

    @endpoints.method(
            RESOURCE_CONTAINER,
            ResponseMessage,
            http_method='PUT',
            path='/resources/{entity_id}'
            )
    def put(self, request):
        return ResponseMessage(
                content=request.content,
                entity_id=request.entity_id,
                query_param=request.query_param
                )

    @endpoints.method(
            message_types.VoidMessage,
            ResponseMessage,
            http_method='GET',
            api_key_required=True,
            path='/resources'
            )
    def get(self, request):
        return ResponseMessage(content='Hello')
