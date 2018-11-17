#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-17 13:25

"""
schema.py
"""


import graphene
from graphene_django.types import DjangoObjectType
from .models import Category, Ingredient, Dish
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField


__author__ = "Toran Sahu <toran.sahu@yahoo.com>"
__license__ = "Distributed under terms of the MIT license"


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ["name", "ingredients"]
        interfaces = (relay.Node,)


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "notes": ["exact", "icontains"],
            "category": ["exact"],
            "category__name": ["exact"],
        }
        interfaces = (relay.Node,)


class DishNode(DjangoObjectType):
    """DishNode Interface Class Provided by Relay."""

    class Meta:
        model = Dish
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "notes": ["exact", "icontains"],
        }
        interfaces = (relay.Node,)


class Query:
    """GraphQL Query Class."""

    dish = relay.Node.Field(DishNode)
    all_dishes = DjangoFilterConnectionField(DishNode)

    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)
