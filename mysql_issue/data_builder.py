#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pymysql
import random
import string
import time
from faker import Faker
import sys

config = {
    "host": "127.0.0.1",
    "user": "root",
    "port": 3306,
    "password": "",
    "database": "test"
}

f = Faker()

def insert_products(num):
    values = []
    i = 0
    size = 100
    big_size = 10240
    while i < int(num):
        i += 1
        productCode = f.isbn13()
        productName = ''.join(random.choices(
            string.ascii_letters + string.digits, k=big_size))
        productLine = f.sentence()
        productScale = f.text()
        productVendor = f.sentence()
        productDescription = f.isbn10()
        quantityInStock = random.randint(1, 1000)
        buyPrice = random.uniform(1.0, 10000.0)
        MSRP = random.uniform(10.0, 20000.0)

        # value = (i, productCode, productName, productLine, productScale,
        #          productVendor, productDescription, quantityInStock, buyPrice, MSRP)
        value = (productCode, productName, productLine, productScale,
                 productVendor, productDescription, quantityInStock, buyPrice, MSRP)
        values.append(value)

    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "INSERT INTO products (productCode, productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    print(sql)
    cursor.executemany(sql, values)
    db.commit()
    cursor.close()
    return 'insert ' + num + ' lines' + "\n"

num = sys.argv[-1]

insert_products(num)
