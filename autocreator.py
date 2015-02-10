#!/usr/bin/env python
from mako.template import Template
from mako.lookup import TemplateLookup
import argparse
import yaml
from os import walk
from jenkins import JenkinsUtils

def serveTemplate(templateName, templateLoc, **kwargs):
  mylookup = TemplateLookup(directories=templateLoc)
  template = mylookup.get_template(templateName)
  return template.render(**kwargs)

def parse_args():
  parser = argparse.ArgumentParser(description="Jenkins command line autocreator")
  parser.add_argument("-d", "--dataLocation", help="The location where your jenkins job data lives", required=True)
  parser.add_argument("-job", "--jobType", help="The types of jobs you wish to create", required=True)
  parser.add_argument("-url", "--jenkinsURL", help="The URL of your jenkins master", required=True)
  parser.add_argument("-a", "--append", help="Optional parameter that will append the value to the end of your job names")
  parser.add_argument("-http", "--http", help="Use this to use http instead of https.  Defaults to https", action="store_true", default=False)
  parser.add_argument("-u", "--username", help="Optional paramater for the username to authenticate against jenkins", required=False, default=None)
  parser.add_argument("-p", "--password", help="Optional paramater for the password to authenticate against jenkins", required=False, default=None)
  args = parser.parse_args()
  return args

def getJobsToBuild(dataDirectory):
  files = []
  for (dirpath, dirnames, filenames) in walk(dataDirectory):
    files.extend(filenames)
    break

  for fileName in files:
    if "default" in fileName:
      files.remove(fileName)
  return files

# Features to add
# The ability to only build a single job (or list of a few jobs) from a job type instead of all the jobs of that type
# Pass port number separately as a separate optional parameter as this may make doing different jenkins auths easier
# Add logging and a verbosity option.  No output right now about what is happening
# Maybe support subdirectories of different "types" so something like acceptance/staging, or acceptance/performance, etc
# Overwrite the job name from within the yml
# Hash the yml and store it locally so we can tell if a job has changed so we dont have to rebuild it


cliArgs = parse_args()
jobType = cliArgs.jobType
dataLoc = cliArgs.dataLocation

if cliArgs.http == True:
  connectionType = "http"
else:
  connectionType = "https"

if cliArgs.append == None:
  appendJobName = ""
else:
  appendJobName = cliArgs.append

jobsLoc = dataLoc + "/" + jobType
dataLoc = [dataLoc, jobsLoc]
jenkins = JenkinsUtils(cliArgs.jenkinsURL, connectionType, cliArgs.username, cliArgs.password)

for job in getJobsToBuild(jobsLoc):
  jobData = serveTemplate(job, dataLoc)
  try:
    jobYML = yaml.load(jobData)
  except:
    print "Yaml failed to parse for file: " + job
    continue    
  jobName = ((jobType + "_" + job).replace(".yml", "") + appendJobName)
  print "\nProcessing the template:  " + jobName
  jenkinsXML = serveTemplate('jenkins.txt', 'templates', **jobYML)
  print "Creating job: " + jobName
  response = jenkins.post_jenkins_job(jenkinsXML, jobName)
  if response.status != 200:
    print "Unable to create job:  " + jobName
    print "   Response code received: " + str(response.status) 


