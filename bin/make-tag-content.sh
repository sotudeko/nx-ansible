#!/bin/bash

cd ../playbooks

#ansible-playbook make-tag-content.yml --extra-vars "scan_report=scan_report.json build_user=sotudeko tag_name=jenkins-Repo-Staging-WebGoat-Example-17 job_id=17 build_url=http://sola.local:8080/job/Repo-Staging/job/WebGoat-Example/17/ build_tag=Repo-Staging/WebGoat-Example build_version=1.0.11 scan_report_url=nnn"

ansible-playbook /Users/sotudeko/Development/github/nxrm-ansible/playbooks/create-tag.yml --extra-vars tag_data=../data/tag_file.json

