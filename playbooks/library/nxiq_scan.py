#!/usr/bin/python

DOCUMENTATION = '''
---
module: nxiq_scan
short_description: Run a Nexus IQ CLI scan
description:
  - Runs the Nexus IQ CLI scan on the specified target
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
  application:
    description:
      - name of the tag (This is mutually exclusive with the body option)
    required: false
    default: null
  target:
    description:
      - name of the tag (This is mutually exclusive with the body option)
    required: false
    default: null
  stage:
    description:
      - name of the tag (This is mutually exclusive with the body option)
    required: false
    default: null
  xc:
    description:
      - name of the tag (This is mutually exclusive with the body option)
    required: false
    default: null
'''

EXAMPLES = '''
- name: list tags (using defaults)
  nxrm_tag_list:
  register: result
'''

from ansible.module_utils.basic import *
import subprocess

java_path = '/usr/bin/java'
iq_cli_path = '/opt/nexus-iq/nexus-iq-cli'

def exec_cli(data):
    has_changed = False

    repo_url = data['repo_url']
    user = data['user']
    password = data['password']
    application = data['application']
    target = data['target']
    stage = data['stage']

    if application is None:
        meta = {'status': -1, 'response': 'no application specified'}
        return (has_changed, meta)

    if target is None:
        meta = {'status': -1, 'response': 'no scan target specified'}
        return (has_changed, meta)

    cmdstr = "{0} -jar {1} -i {2} -s {3} -a {4}:{5} -t {6} {7}".format(java_path, iq_cli_path, application, repo_url, user, password, stage, target)
    return_code = subprocess.call("echo Hello World", shell=True)  
    return (has_changed, {})

def main():

    fields = {
        "user": {"default": "admin", "required": False, "type": "str"},
        "password": {"default": "admin123", "required": False, "type": "str", "no_log": True},
        "repo_url": {"default": "http://localhost:8081", "required": False, "type": "str" },
        "target": {"required": True, "type": "str" },
        "application": {"required": True, "type": "str" },
        "xc": {"default": False, "required": False, "type": "boolean" },
        "stage": {
        	"default": "build", 
        	"choices": ['build', 'stage-release', 'release'],  
        	"type": 'str' 
        } 
	  }

    module = AnsibleModule(argument_spec=fields)
    has_changed, result = exec_cli(module.params)
    module.exit_json(changed=has_changed, meta=result)

if __name__ == '__main__':
    main()

 
