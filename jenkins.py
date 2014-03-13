import httplib
import socket


class JenkinsUtils(object):
  def __init__(self, jenkinsURL, connectionType):
    self.jenkinsURL = jenkinsURL
    self.connectionType = connectionType

  def post_jenkins_job(self, configXML, jobName):
    if self.job_exists(jobName):
      response = self.update_job(jobName, configXML)
    else:
      response = self.create_job(jobName, configXML)

  def job_exists(self, jobName):
    connection = self.create_connection()
    existsURL = "/job/" + jobName + "/config.xml"
    connection.request("GET", existsURL)
    response = connection.getresponse()
    if response.status == 200:
      return True
    else:
      return False

  def create_job(self, jobName, configXML):
    connection = self.create_connection()
    createURL = "/createItem?name=" + jobName
    headers = {"Content-Type" : "text/xml", "Accept": "text/plain"}
    connection.request("POST", createURL, configXML, headers)
    response = connection.getresponse()
    return response

  def update_job(self, jobName, configXML):
    connection = self.create_connection()
    updateURL = "/job/" + jobName + "/config.xml"
    headers = {"Content-Type" : "text/xml", "Accept": "text/plain"}
    connection.request("POST", updateURL, configXML, headers)
    response = connection.getresponse()
    return response

  def create_connection(self):
    if self.connectionType != 'http':
      return httplib.HTTPSConnection(self.jenkinsURL, timeout=20)
    else:
      return httplib.HTTPConnection(self.jenkinsURL, timeout=20)


