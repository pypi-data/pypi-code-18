import SocketServer
import BaseHTTPServer
import SimpleHTTPServer

import requests

def printAuthorName():
    print "Dhruv Thakker"

def getOAuthToken(client_id,client_secret,username,password,grant_type,host):

    url = "http://"+host+"/oauth2/access_token"
    response2 = requests.post(url, {"username": username, "password": password, "client_id": client_id,
                                        "client_secret": client_secret, "grant_type": grant_type})
    print response2

    if response2.status_code==200:
        accessToken= response2.json().get('access_token')
    else:
        print "Unable to get Access Token Try Again"

    return accessToken

def getEnrollmentInfo(host,access_token):

    url = "http://" + host + "/api/enrollment/v1/enrollment"

    header = {'Authorization': "Bearer " + access_token}

    response = requests.get(url, headers = header)

    return response

def getEnrolledInCourse(host,access_token,course_id):

    url = "http://" + host + "/api/enrollment/v1/enrollment"

    header = {'Authorization': "Bearer " + access_token}

    response = requests.post(url, json={
        "course_details": {
            "course_id": course_id
        },
    }, headers = header)

    return response

def getAvailableCourses(host):
    url = "http://" + host + "/api/courses/v1/courses"

    response = requests.get(url)

    return response

def getCourseInfo(host,course_id):
    url = "http://" + host + "/api/courses/v1/courses"

    url = url + "/" + course_id


    response = requests.get(url)

    return response



def startMultiServer(reqPort=None):
    class ThreadingSimpleServer(SocketServer.ThreadingMixIn,
                       BaseHTTPServer.HTTPServer):
        pass
    import sys
    if reqPort:
        port = int(reqPort)
    else:
        port = 8000

    server = ThreadingSimpleServer(('', port), SimpleHTTPServer.SimpleHTTPRequestHandler)

    print "Server Running on you localhost or lan on port :"+port
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print "Finished"
