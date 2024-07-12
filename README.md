# 🛡️SCS - Security IaaS Scan Pipeline

## Introduction

This repository contains the code necessary to recreate the SCS automated pentesting methodology, which allows to scan infrastructure targets  to detect and manage security vulnerabilities, using state-of-the-art tools.

## Features

- Designed for daily and weekly runs
- Based on docker containers
- Port scanning
- Web services identification
- Template based scanning
- Both Fast and Full DAST
- Full infrastructure scanning
- Export of results to a centralized vulnerabilities management system

## Directory Structure
```
- /.zuul.d --> Contains Zuul configuration (jobs definition, global timeouts, secrets, etc)
  |- config.yaml
  |- secrets.yaml
- /docs -> Contains the security documentation for docs.scs.community
  |- overview.md
  |- tools.md   
- /files --> Contains scripts and other needed files
   |- greenbone-compose.yaml
   |- gvm_scan.py
   |- targets.txt
- playbooks --> Contains the definition of tasks for each job
   |- daily-scan.yaml
   |- greenbone.yaml
   |- httpx.yaml
   |- naabu.yaml
   |- nucley.yaml
   |- owasp-zap.yaml
   |- post.yaml
   |- pre.yaml
   |- weekly-scan.yaml
- .gitignore
- README.md
```

## Getting Started

Go through the [documentation](./docs) for details on how the IaaS Scan Pipeline is designed and specific instructions about prerequisites, configuration and/or tweaks.