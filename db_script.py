#!/usr/bin/python
#-*- coding: utf-8 -*-

from sqlalchemy import *
from faker import Factory
import sys, json,random

#Generate Fake data
faker = Factory.create()
# print dir(faker)
# sys.exit(1)
resp = {"success":False, "message":None, "data":None}

try:
    create_db = create_engine('mysql+pymysql://root:test@localhost/', echo=True)
    create_db.execute("CREATE DATABASE kovert_db")
    resp['success']=True
    resp['message']="DB created"
except Exception as e:
    resp['message']="Failed to create! %s" % e
    print resp

try:
    #db = create_engine ( "mysql+pymysql://test@localhost/kovert_db" )
    db = create_engine('mysql+pymysql://root:test@localhost/kovert_db', echo=True)
    connection = db.connect()
    resp['success']=True
    resp['message']="Connected!"
    #print dir(db)
    #print "Connected! %s" % (db.raw_connection)
except Exception as e:
    resp['message']="Failed to connect! %s" % e
    print resp


try:
    metadata = MetaData(bind=db)
    company_table = Table('company', metadata,Column('id',Integer, primary_key=True, nullable=False),
                          Column('name', String(30), nullable=False), 
                          Column('address', String(50),nullable=False), 
                          Column('country', String(30),nullable=False))

    client_table = Table('client', metadata,Column('id',Integer, primary_key=True, nullable=False),
                          Column('name', String(30), nullable=False), 
                          Column('address', String(50),nullable=False))

    company_client_table = Table('company_client', metadata,
                                 Column('company_id', Integer, nullable=False), 
                                 Column('client_id', Integer,nullable=False))

    # create tables in database
    metadata.create_all()

    stats={'num_of_companies_inserted':0, 'num_of_clients_inserted':0, 'num_of_cmp_clients_inserted':0}
    country =["UK", "US"]

    for s in range(10):
        insert = company_table.insert()
        new_company = insert.values(name=faker.company(), address=faker.street_name(), country=random.choice( country ) )        
        #establish database connection
        insert_statement = db.connect()

        # execute insert statement
        insert_statement.execute(new_company)
        stats['num_of_companies_inserted']+=1

    for s in range(50):
        insert = client_table.insert()
        new_client = insert.values(name=faker.name(), address=faker.street_name() )
        
        #establish database connection
        insert_statement = db.connect()

        # execute insert statement
        insert_statement.execute(new_client)
        stats['num_of_clients_inserted']+=1


    s = select([company_table])
    result = s.execute()
    cmp_id={}
    counter = 0
    for cmp_data in result:
        company_data= dict (cmp_data)
        counter = counter + 1
        key = "id_%d" % counter
        cmp_id.update({key:company_data.get('id')})


    s = select([client_table])
    result = s.execute()
    cl_counter = 0
    cl_id= {}
    for row in result:
        cl_counter = cl_counter + 1
        key_cl = "id_%d" % cl_counter
        client_data=dict(row)
        cl_id.update({key_cl:client_data.get('id')})

    cmp_ = len(cmp_id) + 1
    cmp_counter_id = 0
    
    for id in range(len(cl_id)):
        cl_counter_id =id + 1
        cmp_counter_id += 1
        
        for i in xrange(cmp_counter_id):
            if cmp_counter_id == cmp_:
                cmp_counter_id=0
                cmp_counter_id+=1
                continue
        raw = {'company_id':cmp_id.get( "id_%d" % cmp_counter_id ), 'client_id':cl_id.get("id_%d" % cl_counter_id)}
        print raw
        insert = company_client_table.insert()
        new_company_client = insert.values(company_id=cmp_id.get( "id_%d" % cmp_counter_id ), client_id=cl_id.get("id_%d" % cl_counter_id))
            
        #establish database connection
        insert_statement = db.connect()

        # execute insert statement
        insert_statement.execute(new_company_client)
        stats['num_of_cmp_clients_inserted']+=1

    print stats
except Exception as e:
    print e
