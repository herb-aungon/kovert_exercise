#!/usr/bin/env python                                                                                                                                                                                       
#-*- coding: utf-8 -*- 

from flask import Flask,request, render_template, flash, jsonify, make_response, Response, url_for, redirect
import json, copy, xmltodict
from sqlalchemy import *
from jinja2 import Environment, FileSystemLoader

 
app = Flask(__name__)

"""
Flask config for changing Debug mode, SECRET_KEY
"""
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
))


#Used to display errors on webpage
@app.errorhandler( 500 )
def internal_500_error( exception ):
     #app.logger.exception( exception )
     return json.dumps( exception )

@app.errorhandler( 404 )
def internal_404_error( exception ):
     #app.logger.exception( exception )
     return 'exercise page" <br/>\n%s<br/>\n%s' % ( exception, request.url )

@app.errorhandler( 401 )
def internal_401_error( exception ):
     #app.logger.exception( exception )
     return 'exercise page<br/>\n%s<br/>\n%s' % ( exception, request.url )


resp = {"success":False, "message":None, "data":None}

try:
    db = create_engine('mysql+pymysql://root:test@localhost/kovert_db')
    connection = db.connect()
    resp['success']=True
    #print dir(db)
    print "Connected! %s" % (db.raw_connection)
except Exception as e:
    resp['message']="Failed to connect! %s" % e
    print resp

@app.route("/kovert_exercise", methods = [ 'GET' ] )
def home_get():
     #get all company
     company_data=[]
     data_raw="SELECT * FROM company"
     comp_data_raw = db.execute( text( data_raw ))
     for c in  comp_data_raw:
          company_data.append(c)

     #get all client
     client_data=[]
     data_raw_1="SELECT * FROM client"
     cl_data_raw = db.execute( text( data_raw_1 ))
     for b in  cl_data_raw:
          client_data.append(b)

     #get uk company only
     select="SELECT * FROM company WHERE country='UK'"
     result = db.execute( text( select ))
     data =[]

     resp=[]
     uk_id =[]

     uk_company = {}
     for r in result:
          r=dict(r)
          uk_company.update({r.get('id'):r})
          uk_id.append(r.get('id'))

     #get client id using company id linked in company_client tbl
     client_id=[]
     uk_client={}
     uk_client_raw=[]
     for t in range(len(uk_id)):
          client_select=("""SELECT * 
          FROM company_client
          WHERE """) 
          cmp_id = " company_id=%d" % uk_id[-1]
          del uk_id[-1]
          client_select += cmp_id


          client_result=db.execute( text ( client_select ) )
          for c in client_result:
               c=dict(c)
               client_id.append(c.get('client_id'))
               uk_client.update({c.get('client_id'):c})
               uk_client_raw.append(c)

     #get specific client using client id found in the company_client 
     cl_cmp_uk_raw={}
     for x in range(len(client_id)):
          client_select_uk=("""SELECT * 
          FROM client
          WHERE """) 
          cl_id=" id=%d" % client_id[-1]
          del client_id[-1]

          client_select_uk += cl_id

          client_result_uk=db.execute( text ( client_select_uk ) )
          for y in client_result_uk:
               y=dict(y)
               cl_cmp_uk_raw.update({y.get('id'):y})
     data=[]

     #get the necessary field from different dict's and combine in 1 list to be displayed in table
     for keys in uk_client:
          key = uk_client[keys]
          company_id = key.get('company_id')
          client_id = key.get('client_id')
          client = cl_cmp_uk_raw.get(client_id)
          client_name = client.get('name')
          company_details = uk_company.get(company_id)
          company_name = company_details.get('name')
          country = company_details.get('country')
          data.append({"company_id":company_id,"company":company_name, "client_name":client_name,  "client_id":client_id,"country":country})

     return render_template('company.html', comp_client=uk_client_raw, resp=data, company=company_data, client=client_data)


@app.route("/kovert_exercise", methods = [ 'OPTIONS' ] )
def home_options():
     return ''

@app.route("/kovert_exercise/food_items", methods = [ 'GET' ] )
def food_get():
     with open('/home/pi/Desktop/kovert_exercise/food.xml') as fd:
          obj = xmltodict.parse(fd.read())

     return render_template('food_items.html',food_items=obj.get('breakfast_menu').get('food') )

@app.route("/kovert_exercise/food_items", methods = [ 'GET' ] )
def food_options():
     return ''


if __name__ == "__main__":
    app.run(debug=True)
    #app.run()
