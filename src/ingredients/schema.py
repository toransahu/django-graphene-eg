#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-17 13:25

"""
schema.py
"""


import graphene
from graphene_django.types import DjangoObjectType
from .models import Category, Ingredient, Dish, Post
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


class PostNode(DjangoObjectType):
    """PostNode Interface."""

    class Meta:
        model = Post
        filter_fields = {
            "id": ["exact"],
            "title": ["exact", "icontains"],
            "content": ["exact", "icontains"],
        }

        #
        # depricated
        #

        # only_fields = ("title", "content")
        # exclude_fields = ('published', 'owner')
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, id, info):
        """get_node.

        :param id:
        :param info:
        """
        try:
            post = cls._meta.model.objects.filter(id=id)
        except cls._meta.model.DoesNotExist:
            return None

        if post.published or info.context.user == post.owner:
            return post
        return None


class Query:
    """GraphQL Query Class."""

    dish = relay.Node.Field(DishNode)
    all_dishes = DjangoFilterConnectionField(DishNode)

    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)

    my_posts = DjangoFilterConnectionField(PostNode)
    post = relay.Node.Field(PostNode)
    # post = graphene.Field(PostNode, id=graphene.Int(), title=graphene.String())

    def resolve_my_posts(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return Post.objects.none()
        else:
            return Post.objects.filter(owner=info.context.user, **kwargs)
