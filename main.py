#The following code has been referenced from https://pythonspot.com/matplotlib-bar-chart/


import os
from flask import Flask, redirect, render_template, request,make_response
import pypyodbc
import urllib
import json
import hashlib
from copy import deepcopy
import base64
from io import BytesIO
import numpy as np
import pymysql
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

app = Flask(__name__)
dbServerName = "35.192.52.133"
dbUser = "root"
dbPassword = "surajkawthekar"
dbName = "surajdb"
charSet = "utf8mb4"

cusrorType = pymysql.cursors.DictCursor

connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,

                                   db=dbName, charset=charSet, cursorclass=cusrorType)


def graph():
    cursor = connectionObject.cursor()
    success = 'SELECT age,fare from titanic'
    cursor.execute(success)

    result_set = cursor.fetchall()
    age = []
    fare = []
    for row in result_set:
        age.append(row['age'])
        fare.append(row['fare'])
    print(age)
    print(fare)
    X = np.array(list(zip(age, fare)))
    kmeans = KMeans(n_clusters=int(8))
    kmeans.fit(X)
    centroid = kmeans.cluster_centers_
    labels = kmeans.labels_
    img = BytesIO()
    print(age)
    print(fare)
    all = [[]] * 8
    print(all)
    for i in range(len(X)):
        colors = ["b.", "r.", "g.", "w.", "y.", "c.", "m.", "k."]
        plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=3)
        plt.scatter(centroid[:, 0], centroid[:, 1], marker="x", s=150, linewidths=5, zorder=10)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())

    response = make_response(img.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


def barchart1():
    cursor = connectionObject.cursor()
    success = 'SELECT count(*) from titanic where sex="male" and survived ="1" and pclass!=1'
    cursor.execute(success)

    result_set = cursor.fetchall()
    age = []
    for row in result_set:
        age.append(row['count(*)'])

    success1 = 'SELECT count(*) from titanic where sex="male" and survived ="1" and pclass=2'
    cursor.execute(success1)
    result_set1 = cursor.fetchall()
    age1 = []
    for row in result_set1:
        age1.append(row['count(*)'])

    success2 = 'SELECT count(*) from titanic where sex="male" and survived ="1" and pclass=3'
    cursor.execute(success2)
    result_set2 = cursor.fetchall()
    age2 = []
    for row in result_set2:
        age2.append(row['count(*)'])

    objects = ('PC1', 'PC2', 'PC3')
    y_pos = np.arange(len(objects))
    performance = [age[0], age1[0], age2[0]]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Count')
    plt.title('numbers of male survivors')
    plt.show()

    return render_template('viewrange.html')

@app.route('/pie', methods=['GET'])
def piechart1():
    cursor = connectionObject.cursor()
    success = 'SELECT count(*) from titanic where sex="female" and survived ="1" group by pclass'
    cursor.execute(success)

    result_set = cursor.fetchall()
    age = []
    for row in result_set:
        age.append(row['count(*)'])

    labels = ('PC1', 'PC2', 'PC3')
    colors = ['red', 'green', 'blue']
    sizes = [age[0], age[1], age[2]]
    explode = (0.1, 0, 0)

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()

    return render_template('viewrangedquakes.html')

@app.route('/scatter', methods=['GET'])
def graph1():
    return graph()

@app.route('/bar', methods=['GET'])
def bar1():
    return barchart1()

@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
