# SCS automated pentesting

Security has a high priority in modern cloud infrastructures. If you look at it from an automation perspective, a basic distinction of tooling is needed to be considered:

* SAST or Static Application Security Testing: These tools scan code that is checked into e.g. git and are integrated into build pipelines. They only look at static artifacts: code, dependencies, container images.
* DAST or Dynamic Application Security Testing: With dynamic testing, running programs and deployed infrastructure are scanned. This allows to identify vulnerabilities, test infrastructure configuration and analyze the behaviour of running processes.

In this project, the SCS automated pentesting pipeline, we solely focus on DAST. 

## Source

[github.com/SovereignCloudStack/security-infra-scan-pipeline](https://github.com/SovereignCloudStack/security-infra-scan-pipeline).

## Tools

See [the tools page](./tools.md).
