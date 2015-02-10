import httplib
import socket
import base64

class JenkinsUtils(object):
  def __init__(self, jenkinsURL, connectionType, username, password):
    self.jenkinsURL = jenkinsURL
    self.connectionType = connectionType
    self.username = username
    self.password = password

    # setup authentication header
    base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
    self.basicAuth = "Basic " + base64string
  
  def post_jenkins_job(self, configXML, jobName):
    if not self.job_running(jobName):
      if self.job_exists(jobName):
        response = self.update_job(jobName, configXML)
      else:
        response = self.create_job(jobName, configXML)
    return response

  def job_exists(self, jobName):
    connection = self.create_connection()
    existsURL = "/job/" + jobName + "/config.xml"
    headers = {"Authorization": self.basicAuth}
    connection.request("GET", existsURL,"", headers)
    response = connection.getresponse()
    if response.status == 200:
      return True
    else:
      return False

# Fill out this method and force the post_jenkins_job method to only
# create the job if job_running is false
  def job_running(self, jobName):
    return False

  def create_job(self, jobName, configXML):
    connection = self.create_connection()
    createURL = "/createItem?name=" + jobName
    headers = {"Content-Type" : "text/xml", "Accept": "text/plain", "Authorization": self.basicAuth}
    connection.request("POST", createURL, configXML, headers)
    response = connection.getresponse()
    return response

  def update_job(self, jobName, configXML):
    connection = self.create_connection()
    updateURL = "/job/" + jobName + "/config.xml"
    headers = {"Content-Type" : "text/xml", "Accept": "text/plain", "Authorization": self.basicAuth}
    connection.request("POST", updateURL, configXML, headers)
    response = connection.getresponse()
    return response

  def create_connection(self):
    if self.connectionType != 'http':
      connection = httplib.HTTPSConnection(self.jenkinsURL, timeout=30)
    else:
      connection = httplib.HTTPConnection(self.jenkinsURL, timeout=30)
    return connection

