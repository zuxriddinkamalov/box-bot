import os
import traceback
from unicodedata import category
import requests
import jsonschema
import urllib

import uuid

import logging

from math import prod
from types import new_class
from typing import List

from os import stat
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.schemas import billz_response_schema, Product

from core import models
from telegram import models as telegram_models

logger = logging.getLogger()

# Create your views here.

class Test(APIView):
    def get(self, request) -> Response:
        products = models.Product.objects.filter(category__title='Вафельное полотенце')
        content = []
        for product in products:
            # if not product.photo:
            content.append(product.title)
        return Response(content)

class UpdateCatalog(APIView):
    def get(self, request) -> Response:
        logger.info("Sync started...")
        if request.headers.get('Access-Token') != "asdkjhqwiokjnkjnmn1276akjhasdkjh":
            return Response(
                {
                    "error": True,
                    "message": "Access-Token invalid"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJlY29tbWVyY2Utc2l0ZS51eiIsImlhdCI6MTY0MjkzNTMwMSwiZXhwIjoxODAwNzAxNzAxLCJzdWIiOiJhaXNoYWhvbWUuZWNvbW1lcmNldGdib3QifQ.RM2h-8d4KHJc_ellD2we7Ykr7qHqQ5x9L2Q45L3FHlQ"
        response = requests.post(
            "https://api.billz.uz/v1/",
            json={
                "jsonrpc": "2.0",
                "method": "products.get",
                "params": {
                    "paramName_1": "paramValue_1",
                    "paramName_2": "paramValue_2"
                },
                "id": "1"
            },
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        payload = response.json()
        try:
            jsonschema.validate(payload, billz_response_schema)
        except jsonschema.ValidationError as e:
            return Response({
                "message": "Invalid billz schema recieved",
                "payload": e.message
            })

        products: List[Product] = []
        for row in payload.get("result"):
            try:
                products.append(
                    Product(**row)
                )
            except Exception as e:
                logger.error(row)
                logger.error(e)

        categories = []
        for product in products:
            category = product.properties.get("CATEGORY")
            if category:
                if category not in categories:
                    categories.append(category)
        
        branches = []
        for product in products:
            for branch in product.offices:
                if branch["officeName"] not in branches:
                    branches.append(branch["officeName"])

        logger.info(f"Got {len(products)} products")
        logger.info(f"Got {len(categories)} categories")
        logger.info(f"Got {len(branches)} branches")

        updated = 0
        created = 0
        error_on_update = 0
        error_on_create = 0
        for product in products:
            try:
                test_product = models.Product.objects.get(external_id=product.ID)
                try:
                    update_product(product, test_product)
                    updated += 1
                except Exception as e:
                    traceback.print_exc()
                    logger.error(e)
                    error_on_update += 1
            except models.Product.DoesNotExist:
                try:
                    create_new_product(product)
                    created += 1
                except Exception as e:
                    traceback.print_exc()
                    logger.error(e)
                    error_on_create += 1



        return Response({
            "created": created,
            "updated": updated,
            "error_on_update": error_on_update ,
            "error_on_create": error_on_create
        })


def update_product(product: Product, product_for_update: models.Product) -> models.Product:
    language = models.Language.objects.all().first()

    product_for_update.title = product.name
    product_for_update.code = f"billz{product.ID}"
    category_product = product.properties.get("CATEGORY")
    product_branches = product.offices
    if category_product:
        try:
            category = models.Category.objects.get(title=category_product, language=language)
        except models.Category.DoesNotExist:
            category = models.Category()
            category.title = category_product
            category.code = str(uuid.uuid4())
            category.language = language
            category.description = category_product
            category.photo = models.Photo.objects.get(title='not_found')
            category.active = True
            try:
                order = models.Category.objects.all().order_by("-order")[0].order + 1
            except Exception as e:
                order = 1
            category.order = order
            # category.save()
    else:
        category = models.Category.objects.get(code="unknown")
    
    if product.offices:
        for office in product.offices:
            try:
                branch = telegram_models.Branch.objects.get(title=office["officeName"])
            except telegram_models.Branch.DoesNotExist:

                region = models.Region.objects.all().first()

                branch = telegram_models.Branch()
                branch.title = office["officeName"]
                branch.external_id = office["officeID"]
                branch.description = office["officeName"]
                branch.region = region
                branch.active = True

                branch.save()

    product_for_update.category = category
    product_for_update.language = language
    product_for_update.description = product.name
    product_for_update.price = product.price
    product_for_update.sku = product.sku
    product_for_update.barcode = product.barCode
    product_for_update.external_id = product.ID
    if product.imageUrls:
        image = product.imageUrls[0]["url"]
        product_for_update.photo = get_image(image)
    else:
        product_for_update.photo = models.Photo.objects.get(title='not_found')
    product_for_update.active = True
    product_for_update.order = product.ID
    product_for_update.save()

    # test_product = models.Product.objects.all().first()
    return product_for_update


def create_new_product(product: Product) -> models.Product:
    language = models.Language.objects.all().first()

    # logger.info(product)

    new_product = models.Product()
    new_product.title = product.name
    new_product.code = f"billz{product.ID}"
    category_product = product.properties.get("CATEGORY")
    product_branches = product.offices
    if category_product:
        try:
            category = models.Category.objects.get(title=category_product, language=language)
        except models.Category.DoesNotExist:
            category = models.Category()
            category.title = category_product
            category.code = str(uuid.uuid4())
            category.language = language
            category.description = category_product
            category.photo = models.Photo.objects.get(title='not_found')
            category.active = True
            try:
                order = models.Category.objects.all().order_by("-order")[0].order + 1
            except Exception as e:
                order = 1
            category.order = order
            # category.save()
    else:
        category = models.Category.objects.get(code="unknown")
    
    if product.offices:
        for office in product.offices:
            try:
                branch = telegram_models.Branch.objects.get(title=office["officeName"])
            except telegram_models.Branch.DoesNotExist:

                region = models.Region.objects.all().first()

                branch = telegram_models.Branch()
                branch.title = office["officeName"]
                branch.external_id = office["officeID"]
                branch.description = office["officeName"]
                branch.region = region
                branch.active = True

                branch.save()

    new_product.category = category
    new_product.language = language
    new_product.description = product.name
    new_product.price = product.price
    new_product.sku = product.sku
    new_product.barcode = product.barCode
    new_product.external_id = product.ID
    if product.imageUrls:
        image = product.imageUrls[0]["url"]
        new_product.photo = get_image(image)
    else:
        new_product.photo = models.Photo.objects.get(title='not_found')
    new_product.active = True
    new_product.order = product.ID
    new_product.save()

    # test_product = models.Product.objects.all().first()
    return new_product


def get_image(url: str) -> models.Photo:
    title = url.split("/")[-1]
    
    try:
        photo = models.Photo.objects.get(title=title)
    except models.Photo.DoesNotExist:
        path = os.path.join(os.getcwd(), 'images', 'tmp', title)
        file = open(path, 'wb')
        file.write(requests.get(url).content)
        file.close()

        photo = models.Photo()
        
        photo.title = title
        with open(path, "rb") as file:
            photo.photo.save(title, file)
        photo.save()
        os.remove(path)

    return photo
    
