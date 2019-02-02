#!/usr/bin/python

DOCUMENTATION = '''
---
module: nxrm_tag_associate
short_description: List all tags in a Nexus Repository
description:
  - Interacts with the specified Nexus Repository 3 instance to list all tags
options:
  repo_url:
    description:
      - HTTP or HTTPS URL in the form of (http|https)://host:domain[:port]
    required: true
    default: http://localhost:8081
  user:
    description:
      - user name to use to log in to Nexus Repository
    required: true
    default: admin
  password:
    description:
      - user password to log in to Nexus Repository
    required: true
    default: admin123
  repo_url:
    description:
      - HTTP or HTTPS URL in the form of (http|https)://host:domain[:port]
    required: true
    default: http://localhost:8081
  tag_name:
    description:
      - name of the tag
    required: true
    default: null
  repo_name:
    description:
      - name of the repository containing the component
    required: true
    default: null
  format:
    description:
      - format of the component repository
    required: true
    default: null
    choices: [ maven ]
  groupId:
    description:
      - component group id
    required: true
    default: null
  artifactId:
    description:
      - component artifact id
    required: true
    default: null
  version:
    description:
      - component version
    required: true
    default: null
'''

EXAMPLES = '''
- name: associate tag with component
  nxrm_tag_associate:
    repo_name: "staging"
    tag_name: "MY-TAG"
    groupId: "org.demo"
    artifactId: "helloworld"
    version: "1.0.1"
    format: "maven"
  register: result
'''

from ansible.module_utils.basic import *
import requests

from requests.auth import HTTPBasicAuth

tags_api = '/service/rest/v1/tags/associate'

def associate_not_yet(data):
  has_changed = False
  meta = {"status": 0, 'response': 'not yet implemented'}
  return (has_changed, meta)

def associate_maven_tag(data):
    has_changed = False

    repo_url = data['repo_url']
    repo_name = data['repo_name']
    tag_name = data['tag_name']

    user = data['user']
    password = data['password']

    groupId = data['groupId']
    artifactId = data['artifactId']
    version = data['version']

    if groupId is None:
        meta = {'status': -1, 'response': 'no groupId specified'}
        return (has_changed, meta)

    if artifactId is None:
        meta = {'status': -1, 'response': 'no artifactId specified'}
        return (has_changed, meta)

    if version is None:
        meta = {'status': -1, 'response': 'no version specified'}
        return (has_changed, meta)

    url = "{}{}{}{}" . format(repo_url, tags_api, '/', tag_name)
    headers = {"Content-Type": "application/json", "accept": "application/json"}

    payload = {'repository': repo_name, 'maven.groupId': groupId, 'maven.artifactId': artifactId, 'maven.baseVersion': version}

    result = requests.post(url, params=payload, auth=(user, password), headers=headers)
    meta = {"status": result.status_code, "response": result.content}

    if result.status_code == 200:
        has_changed = True

    return (has_changed, meta)

def main():

    fields = {
        "user": {"default": "admin", "required": False, "type": "str"},
        "password": {"default": "admin123", "required": False, "type": "str", "no_log": True},
        "repo_url": {"default": "http://localhost:8081", "required": False, "type": "str" },
        "tag_name": {"required": True, "type": "str"},
        "repo_name": {"required": True, "type": "str"},
        "groupId": {"required": False, "type": "str"},
        "artifactId": {"required": False, "type": "str"},
        "version": {"required": False, "type": "str"},
        "format": {
        	"required": True, 
        	"choices": ['maven', 'npm', 'python', 'docker', 'nuget'],  
        	"type": 'str' 
        }
    }

    format_map = {
      "maven": associate_maven_tag,
      "npm": associate_not_yet,
      "python": associate_not_yet,
      "docker": associate_not_yet,
      "nuget": associate_not_yet,
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, result = format_map.get(module.params['format'])(module.params)
    module.exit_json(changed=has_changed, meta=result)

if __name__ == '__main__':
    main()

 
