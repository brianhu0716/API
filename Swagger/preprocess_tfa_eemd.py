# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class PreprocessTfaEemd(Resource):

    def get(self):
        print(g.args)

        return {'message': 'something'}, 200, None

    def post(self):
        print(g.json)

        return {'message': 'something'}, 200, None

    def delete(self):
        print(g.args)

        return {'message': 'something'}, 200, None