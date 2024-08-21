# Quickstart

This page covers the process of setting up an IaaS layer automated pentesting pipeline.

The provided configuration options result in a simple and working deployment that allows to scan a set of defined targets. However, it is possible to adapt each tool behaviour adding additional capabilities, which are defined in their specific documentation.

## Prerequisites

- DefectDojo instance available. See [defectdojo repo](https://github.com/SovereignCloudStack/defectdojo) for deployment instructions.

- Zuul instance available and configured with daily and weekly timed pipelines. See [zuul repo](https://github.com/SovereignCloudStack/zuul), [zuul-scs-jobs repo](https://github.com/SovereignCloudStack/zuul-scs-jobs) and [zuul community docs](https://docs.scs.community/community/tools/zuul/) for deployment instructions and examples.

## Configuration

### DefectDojo

After installing DefectDojo, a few key configurations are necessary to start using the platform effectively, ensuring that a streamlined process for managing security assessments, tracking vulnerabilities, and integrating with existing tools and processes is set up based on SCS Standards.

- **Products**:
  - Definition: In DefectDojo, a "Product" represents an application, system, or any entity that is being tested or tracked for vulnerabilities.
  - Configuration: 
    - Navigate to the "Products" section and click "Add Product."
    - Fill in the necessary details such as the product name, description, and criticality.
    - Assign product type, enable/disable tracking of findings, and set the product's authorization configuration.
- **Engagements**:
  - Definition: An "Engagement" refers to a specific instance of testing or assessment activity against a product. This could be a penetration test, vulnerability assessment, or any other security-related activity.
  - Configuration:
    - In the "Engagements" section, click "Add Engagement."
    - Choose the product you want to engage with, define the type of engagement (e.g., pen test, code review), and set the time frame.
    - Once created, note the engagement id that has been generated, as it will be needed for pipeline configuration (just pick the id number from the URL, in the form of ```https://<instance_url>/engagement/<engagement_id>```)
    - Optionally, link the engagement to an external test plan, define test lead, and add team members.
   - **Recommended setup**: Add at least the following engagements.
     - *Daily Automated Scan*
     - *Weekly Automated Scan*

- **Importing Findings from Tools**:
  - Definition: DefectDojo can import findings from various security tools, allowing centralized tracking and management.
  - Configuration:
    - Tasks on the automated pipelines leverage DefectDojo API to automate imports by sending scan results directly to the system using specific endpoints for supported tools.
    - The import POST request to the api needs to be authenticated. Several methods are availiable, but taking into accounts security measures, the use of tokens/keys are encouraged.
    - To get a working API key, under user menu head to "*API v2 Key*" or directly access the endpoint ```https://<instance_url>/api/key-v2```. If it is needed, generate a new one.
    - Alternatively, it is possible to use the "Import Scan Results" option within an engagement to manually import results from tools like OWASP ZAP, Burp Suite, Nessus, etc.
  
- **User and Role Management**:
  - Configuration: 
    - It is possible to directly set up users and assign roles (Admin, Staff, Developer, etc.) based on the level of access required. Using Keycloak based login is encouraged.
    - Manage permissions and ensure users have the correct access to products, engagements, and reports.
  
- **Notifications and Reports**:
  - Configuration:
    - Set up notifications to alert users about new findings, engagement updates, or product changes.
    - Generate reports to summarize findings, trends, and metrics for stakeholders.


### Zuul

Based on how the jobs and tasks are defined across the automated scan pipelines, it is neccesary to define some variables and secrets at Zuul level in the ```.zuul.d/``` folder of the repo.

- **config.yaml**
  - This file contains project specific zuul configuration related to jobs. 
  - During checks, the pipeline is run with a mock test configuration in order to debug canges and determine if it works as expected.
  - Configuration:
    - ```scan_targets``` variable, under ```scs-security-scan-base``` job, controls what will be scanned. ***Only use IPv4 addresses and/or full domain names*** (Otherwise pipeline will fail). 
    - It is mandatory to set ```timeout``` values based on the targets being defined for scanning, especially for the ```scs-greenbone-security-scan-base``` job, as greenbone ecosystem deployment and full scanning takes a very long time, which could cause workers to finish earlier than expected.
  
  <!-- *NOTE(90n20): Due to zull recent changes now secrets are stored in Vault, hence the use of encrypted secrets in git is deprected as explained in https://github.com/SovereignCloudStack/zuul-scs-jobs?tab=readme-ov-file#secrets* -->
- **secrets.yaml**
  - This file contains encrypted variables which may contain sensitive data:
    -  ```dojo_api_key```: API Token generated during DefecDojo configuration. 
    -  ```dojo_url```: DefecDojo endpoint for importing scans in the form of ```https://<instance_url>/api/v2/import-scan/```.
    -  ```daily_scan_engagement_id```: Engagement id for daily scans generated during DefecDojo configuration.
    -  ```weekly_scan_engagement_id```: Engagement id for weekly scans generated during DefecDojo configuration.
  - In order to generate secrets it is recommended to use zuul-cli tool. As an example: ```echo -n "secret" | zuul-client --zuul-url https://zuul.sovereignit.cloud encrypt --tenant scs --project SovereignCloudStack/security-infra-scan-pipeline  --field-name <variable_name>```

### Aditional notes

With this configuration pipeline should work with its default configuration, uploading each scan results to DefctDojo for further analysis and tracking of the vulnerabilities found.

However, depending on user needs, it is possible to leverage included tools functionalities modifying the command being launched in their respective playbook. Options include, but not limited to, ports being scanned, requests rate-limit, threads spawned, templates/rules being used or response codes filtering, among others.

This provides a complete and very customizable toolkit to perform vulnerability assessments across a wide range of targers.

For further details refer to each tool official documentation.