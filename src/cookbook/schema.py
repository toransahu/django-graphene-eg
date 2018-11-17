#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-17 13:44

"""
schema.py
"""


import graphene
from ingredients.schema import Query as IngredientQuery


__author__ = "Toran Sahu <toran.sahu@yahoo.com>"
__license__ = "Distributed under terms of the MIT license"


class Query(IngredientQuery, graphene.ObjectType):
    """Project level Query class."""

    pass


schema = graphene.Schema(query=Query)
