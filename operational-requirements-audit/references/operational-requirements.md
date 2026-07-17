# Findmypast Operational Requirements (bundled reference)

Extracted from 29 OR pages exported from Discourse. Each entry below is the
FIRST post of the OR's Discourse thread only (the requirement definition) -- later
discussion/replies in the original thread are intentionally omitted.

Regenerate with `python scripts/extract_ors.py <ors_dir> references/operational-requirements.md`
when the source OR export is refreshed.


## Automated Testing

### Acceptance testing _ critical path tests
<!-- source: Automated Testing_ Acceptance testing _ critical path tests - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Service must implement this requirement. (Where appropriate.)

All services should have BDD style acceptance tests that validate the end to end user UI journeys associated with your service. Acceptance tests should be executed as part of the Teamcity deployment pipeline and the pipeline should be stopped if the Acceptance tests fail.

If your service affects any of the critical path tests - registration, login, payments, searching, etc - ensure that the critical path tests are updated to reflect changes introduced by the service.Your service should also run the critical path tests as part of the deployment pipeline.

BDD UI tests written in [Gherkin](https://docs.cucumber.io/gherkin/) are encouraged since the tests are written in plain English and can become living documentation for a service.

### BDD stye integration tests
<!-- source: Automated Testing_ BDD stye integration tests - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this requirement.

All services should have BDD style integration tests testing the business rules of the service. These tests should be executed as part of the Teamcity pipeline and the pipeline should stop if the tests fail.

BDD Integration tests written in [Gherkin](https://docs.cucumber.io/gherkin/) are encouraged since the tests are written in plain English and can become living documentation for a service.

### Unit tests
<!-- source: Automated Testing_ Unit tests - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

All services should have unit tests that are executed on pre-push git hook and also within the Teamcity build.

Failing tests should stop the commit being pushed to github.

Failing tests within the Teamcity build should stop the deployment pipeline.


## Dashboards

### Service should have a Business Metric dashboard
<!-- source: Dashboards_ Service should have a Business Metric dashboard - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

All services should have a agreed [Service Level Objectives](https://discourse.findmypast.com/t/service-must-have-defined-and-monitored-performance-service-level-objectives/699) (SLO) which include instrumenting business metrics.

Business metrics should be visualised on a dashboard using Grafana (or equivalent). The dashboard should clearly show how the business metrics are performing against the SLO.

### Service should have an operational dashboard
<!-- source: Dashboards_ Service should have an operational dashboard - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

All services should have a agreed [Service Level Objectives](https://discourse.findmypast.com/t/service-must-have-defined-and-monitored-performance-service-level-objectives/699) (SLO) which include instrumenting operational metrics such as error rate, requests per sec, latency, etc.

Operational metrics should be visualised on a dashboard using Grafana (or equivalent). The dashboard should clearly show how the operational metrics are performing against the SLO.


## Databases

### Databases must have an automated migration system in place run from CI
<!-- source: Databases_ Databases must have an automated migration system in place run from CI - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this Operational Requirement _if_ your service uses a database.

Changes to the database schema, new data, updates to stored procedures, indexes, etc must be automated, [idempotent](https://en.wikipedia.org/wiki/Idempotence) and managed via a database migration tool, and runnable via continuous integration.

### Databases must have backups
<!-- source: Databases_ Databases must have backups - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR  _if_  your service uses a database.

All SQL and Postgres databases are automatically backed up by the operations team.

If you use a different backend store, you should work with Spanners / Operation steam to ensure that your data is backed up on a regular basis.

### Databases must have failover redundancy
<!-- source: Databases_ Databases must have failover redundancy - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR  _if_  your service uses a database **and** your service is a top tier service

Legacy C#.Net code is tied to our legacy MS-SQL database which currently does not have any failover redundancy. For new services that are de-coupled from MS-SQL and use databases like Postgres, it is recommended that the database is setup for high availability (HA). If the lead server becomes unavailable, one of the follower servers’ will take the lead. Without HA, we run the risk of an outage while we restore the database server.

You must implement HA if your service is a top-tier service (critical to the running of FMP). Spanners team can provision and get you started with a HA Postgres setup.

### Databases must have restore plan in place
<!-- source: Databases_ Databases must have restore plan in place - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR  _if_  your service uses a database.

For MS-SQL and Postgres databases, Spanners / Operations have restore procedures in place. Contact Spanners for more details on restoring Postgres databases. Operations team can deal with MS-SQL databases.

If your service is using a backend store that is not MS-SQL or Postgres, then your service TSG must reference how to restore the database should disaster happen.

### Databases must run a test restore once a quarter
<!-- source: Databases_ Databases must run a test restore once a quarter - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR  _if_  your service uses a database.

Spanners run a test restore of a Postgres database once a quarter. However, you should schedule time with the Spanners team to test the restore of your service (Postgres) data once a quarter.

At this moment, test restore of MS-SQL databases are being performed.


## Deployment and Release

### CI Pipeline
<!-- source: Deployment and Release_ CI Pipeline - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

Service must have a fully automated & reliable deployment pipeline that supports trunk based development and continuous deployment

A CI pipeline should be in place for all services. The pipeline should support continuous deployment from the master branch of the service repository.

The pipeline should, at the least:

- Build & test the service. If the test fails, the build fails

- Deploy the service to a staging environment and run both the integration and critical UI path tests. Failures should break the build.

- Deploy to production

- Tag the release in Github

### Feature Toggles
<!-- source: Deployment and Release_ Feature Toggles - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

New features must have feature toggles in order to mitigate incidents quickly

When updating a service with a new feature, ensure that the feature can be enabled or disabled quickly and easily by using a LaunchDarkly feature toggle. A feature toggle is also necessary for any experimentation.

A description of all feature toggles and their intended use should be documented in the readme and in the service TSG.


## Developer Experience

### Service must have a command for debugging service locally
<!-- source: Developer experience_ Service must have a command for debugging service locally - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Services must implement this operational requirement.

Each service should have a command that starts a debugger or the service should provide configuration for an editor (such as VSCode) which is configured to easily allow the service to be started and debugged from within the editor.

Details on how to debug the service should be documented in the readme.

### Service must have automated setup for running locally
<!-- source: Developer Experience_ Service must have automated setup for running locally - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Services must implement this operational requirement.

Each service should have a setup process that initialises the service for local development. Typically this is performed via an usher task - `usher run setup_local`.

Once setup, engineers should be able to start up the service locally with one command, such as `npm start` or `usher run local`

The service should just work from the command line with no extra configuration required (such as providing vault access keys or environment variables).


## Documentation

### An engineer from outside your team must be able to follow TSG for service_feature
<!-- source: Documentation_ An engineer from outside your team must be able to follow TSG for service_feature - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

Your service should include a comprehensive trouble shooting guide (TSG) that provides details on how to diagnose and solve common problems.

Different engineers have different levels of experience with certain areas of the FMP infrastructure; what’s clear to one engineer may not be clear to others. In order to ensure clarity of the troubleshooting steps, you must get your TSG reviewed by engineers who have little knowledge of the service.

### Service must have a Trouble shooting guide
<!-- source: Documentation_ Service must have a Trouble shooting guide - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

Your service should include a comprehensive trouble shooting guide (TSG) that provides details on how to diagnose and solve common problems.

Note that if your service has alerts, there should be a corresponding section in your TSG to details how to fix the alert.

### Service must have a readme that indicates what a service performs and how to run
<!-- source: Documentation_ Service must have a readme that indicates what a service performs and how to run - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

The service should have a README that is understandable by members of engineering that are not familiar with the service. That is, it should explain what the service does, why it exists, etc. Jargon / abbreviations should always be disambiguated on their first use or via a linked glossary.

The README should be regularly reviewed, preferably by another team.

Some examples of good README’s are:

- [https://github.com/findmypast/customer-service-ui](https://github.com/findmypast/customer-service-ui)

- [https://github.com/findmypast/customer-service-api](https://github.com/findmypast/customer-service-api)

- [https://github.com/findmypast/atlas](https://github.com/findmypast/atlas)

- [https://github.com/findmypast/titan/blob/master/documentation/nygb.md](https://github.com/findmypast/titan/blob/master/documentation/nygb.md)


## Logging and Instrumentation

### Distributed Tracing
<!-- source: Logging and Instrumentation_ Distributed Tracing - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR operational requirement. Services must implement this requirement.

Service should forward the relevant headers for distributed tracing.

Services should enable the Istio proxy sidecar for their pods. The sidecar enables the use of services such as distributed tracing. This is simply a metadata annotation on your deployment manifest. See [Flipper manifest](https://github.com/findmypast/flipper/blob/master/helm/templates/deployment.yaml#L23) for an example.

Services should store tracing headers from incoming requests and forward all the tracing headers to each outgoing HTTP request:

- x-request-id

- x-b3-traceid

- x-b3-spanid

- x-b3-parentspanid

- x-b3-sampled

- x-b3-flags

- x-ot-span-context

If all is well, we should see the trace requests appearing in [Jaegar](http://jaeger.integration.service.dun.fh/search).

Note: At the moment distributed tracing should only be enabled on the staging cluster.

See also: [Distributed Tracing guide](https://github.com/findmypast/guides/blob/master/infrastructure/istio/distributed-tracing.md).

### Log All Failures
<!-- source: Logging and Instrumentation_ Log All Failures - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR operational requirement. Services must implement this requirement.

Service must log errors and other failures

The [logging and instrumentation guidelines](https://github.com/findmypast/guides/tree/master/infrastructure/logging) provides best practice advice for logging.

Errors that crash the pod will be logged to Graylog, but the error message and associated stack trace is split into multiple log entries making it hard to read. It is strongly recommend that your service catches all errors and adds contextual information to the log entry. Take care to format the message correctly, especially if you are adding a stacktrace.

You should also take the opportunity to migrate the service logging code to use the  K8s approach to logging. Details are in the logging guide, but in general:

- Remove any modules that are specific to Graylog or GELF logging.

- Update your code to send your logs to stdout/stderr. These still need to be JSON formatted logs

- Remove the following metadata fields from the log: `application`, `source`, `service_node`, `environment` and `colour`. These are automatically populated.

### Report Business Metrics
<!-- source: Logging and Instrumentation_ Report Business Metrics - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR operational requirement. Services must implement this requirement.

Service must report business level metrics for the feature(s) that it performs. Business metrics should focus on what business objective of the service. E.g.: Account service should think about metrics like number of successful sign-ins, number of failed sign-ins, number of successfully registrations, number of failed registrations, etc.

Instrumenting these metrics allows us to:

- Visualise how well the service is meeting it’s business objective

- Spot patterns in abnormal behaviour. E.g.: Number of failed registration attempts has risen signifcantly.

- Alert on abnormal behaviour. E.g.: Number of sign-ins has reduced significantly

Your [SLO](https://discourse.findmypast.com/t/service-must-have-defined-and-monitored-performance-service-level-objectives/699) should detail the business metrics that it needs to produce.

The [logging and instrumentation guidelines](https://github.com/findmypast/guides/tree/master/infrastructure/logging) provides advice on how to use Prometheus metrics to instrument metrics for your service.

### Report Performance Metrics
<!-- source: Logging and Instrumentation_ Report Performance Metrics - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR operational requirement. Services must implement this requirement.

Service must report performance metrics

Your [SLO](https://discourse.findmypast.com/t/service-must-have-defined-and-monitored-performance-service-level-objectives/699) should detail the operational metrics that it needs to produce. Operational metrics would include:

- Service up time

- Number of incoming requests

- Duration of the requests

- Number of requests that error

The [logging and instrumentation guidelines](https://github.com/findmypast/guides/tree/master/infrastructure/logging) provides advice on how to use Prometheus metrics to instrument your service.


## Monitoring and Alerting

### Alert fires on unavailable service
<!-- source: Monitoring and Alerting_ Alert fires on unavailable service - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR operational requirement. Services must implement this requirement.

The service must create an alert that fires if the service is down for a defined period of time. The alert should either page the on-call engineer via VictorOps (for critical service) or send a message to a monitored Slack channel (non-critical service).

Here’s a [guide of creating alerts with Prometheus](https://github.com/findmypast/guides/blob/master/infrastructure/k8s/alerting-with-prometheus.md).

The service [SLO](https://discourse.findmypast.com/t/service-must-have-defined-and-monitored-performance-service-level-objectives/699) should define how to plan to determine service unavailability. Prometheus provides a lot of metrics about the service and the pods that are running (or not running!) within the cluster.

 There is an existing alert in place that determines when the [number of pod replicas falls below 50%](https://github.com/findmypast/k8s-ansible/blob/master/manifests/alerting/alerts/replicas-not-running-alert.yml). You may wish to take that and customise it for your own needs.

Alternatively, use the `up` metric to determine if the service is contactable via Prometheus. E.g.: `1-avg(rate(up{service="flipper"}[10m]))` returns a percentage availability for the last 10min . 1 == the service is 100% available.

Note this just means that Prometheus can scrape the metrics, it does not mean the service is performing as expected. You may want to choose another metric to determine service availability.

### Alerts must indicate the service affected & problem being experienced
<!-- source: Monitoring and Alerting_ Alerts must indicate the service affected & problem being experienced - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

Alerts must contain enough detail to inform the on-call engineer which service is alerting and what the problem is with the service. It is **strongly** encouraged to use Prometheus alerting, since this will allow us to add richness to the alert, such as a link to the TSG, Graylog, etc. Here’s an example:

See also:

- The [Alerting with Prometheus](https://github.com/findmypast/guides/blob/master/infrastructure/k8s/alerting-with-prometheus.md) guide

### Create Business Metrics Alerts
<!-- source: Monitoring and Alerting_ Create Business Metrics Alerts - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR operational requirement. Services must implement this requirement

Your service should create alerts that must fire if a Service’s [business level metrics](https://discourse.findmypast.com/t/logging-and-instrumentation-report-business-metrics/716) are not performing as expected.

Alerts should either page the on-call engineer via VictorOps (critical service) or send a message to a monitored Slack channel (non-critical service).

For Prometheus alerts, please follow the [guide on how to creating alerts with Prometheus](https://github.com/findmypast/guides/blob/master/infrastructure/k8s/alerting-with-prometheus.md). This will ensure that your alert follows best practice. E.g.: The service name is clear from the alert, it has a link to a TSG to disagnose the issue, etc.

Your [SLO](https://discourse.findmypast.com/t/service-must-have-defined-and-monitored-performance-service-level-objectives/699) should define the business metrics and the operational metrics that it needs to produce.

### Service must have health check endpoints + heartbeats to test _ record external dependencies
<!-- source: Monitoring and Alerting_ Service must have health check endpoints + heartbeats to test _ record external dependencies - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

Services running in K8s must have a [liveness probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-liveness-command) endpoint configured to allow K8s to restart the pod on failure.

Additionally, it is useful to define an endpoint that returns the state of any dependencies of the service. for example, [Raiser’s readiness endpoint](http://raiser.production.service.dun.fh/_health) also reports the state of it’s dependent services:

`Victorops is OK
Slack API is OK
Database connection is OK
`

However, this is just a visual reference. You should be careful if you are using the readiness probe to report upstream state. You should not fail the readiness probe if, for example, a database is not available. This will result in all your K8s pods failing to restart. Instead, the service should handle the failure of the database gracefully, instrument the failure and alert on the failure.

For services outside of K8s, you should implement a heartbeat / health check for your service and ensure that the heartbeat is checked requalry. One way of implementing this is to [create an HTTP alert in Icinga](https://github.com/findmypast/guides/tree/master/infrastructure/alerting-icinga#http-alerts).


## Resilience and Stability

### Failover redundancy
<!-- source: Resilience and Stability_ Failover redundancy - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR operational requirement. Services must implement this requirement.

Service must have failover redundancy (e.g. minimum 3 running containers)

Services should have at least three running pods within K8s in order to cater for unexpected issues, such as the K8s worker node hosting your pod becoming unavailable.

In general, your SLO should detail what is the minimum acceptable performance for your service, so your service may require more than 3 pods to meet your SLO if it is under heavy load. The team should test the performance of the service under load and adjust the number of pods accordingly. Note, your service should also [implement pod autoscaling](https://discourse.findmypast.com/t/resilience-and-stability-horizontal-scaling/714) to dynamically increase/decrease the number of pods depending on load.

If your service has a small number of pods, then during deployment the total number of available pods may be lower than the minimum. For example, for a service with 3 pods, during deployment at least one pod will be deleted while the new pod is created. For a short while, the service will be running with only 2 pods. You can mitigate this by tweaking the `maxSurge` and `maxUnavailable` in your Helm deployment YAML files. For example, setting `maxSurge=1` and `maxUnavailable=0` will first create a new pod during deployment. Once that new pod is running then it will delete one of the other three pods.

### Handle upstream failures
<!-- source: Resilience and Stability_ Handle upstream failures - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR operational requirement. Services must implement this requirement.

Services must be resilient to an upstream service failure and should not be contribute to cascading failure scenarios

Services should deal with upstream service failures - heavy load can cause upstream services to be slow and timeout or network issues may cause intermittent connection problems.

When an upstream service fails, your service should deal with the failure gracefully and **not** contribute to a cascading failure scenario.

Service are encouraged to investigate using the circuit breaker pattern to manage load on slow upstream services. (Note that within K8s, Istio can provide [circuit breakers](https://istio.io/docs/tasks/traffic-management/circuit-breaking/) on behalf of your service.

Teams should also use Istio’s [fault injection](https://istio.io/docs/tasks/traffic-management/fault-injection/) to help test your service response to slow or broken HTTP connections to upstream services. Contact Spanners for guidance on how to configure and test broken/slow network requests.

### Horizontal Scaling
<!-- source: Resilience and Stability_ Horizontal Scaling - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR operational requirement. Services must implement this requirement.

Service must be designed to be horizontally scalable to cope with increases in load/usage

Services should have at least three running pods within K8s in order to cater for unexpected issues, such as the K8s worker node hosting your pod becoming unavailable.

The Kubernetes [horizontal pod autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) should be used here to dynamically scale the number of pods depending on load. The horizontal scaler will ensure that a minimum number of pods are available, scaling up and creating new pods when certain thresholds are exceeded. The horizontal scaler will also scale down if load reduces,


## Service Level Objectives

### Service must have defined and monitored performance Service Level Objectives
<!-- source: Service must have defined and monitored performance Service Level Objectives - Engineering _ Service OR - Findmypast.html -->

This is a MAJOR requirement. Your service must implement this OR.

You should define both operational and business service level objective here. Operational metrics would include:

- Service up time (availability)

- Number of incoming requests (load)

- Duration of the requests (latency of requests)

- Number of requests that error (ratio of success vs failed requests)

Your business metrics are specific to your service, so think careful about what metrics you can define that you can later instrument (and alert on) if the service is failing to meet it’s business requirements.

For example, a registration and sign-in service would have business metrics for the number of successful registration, failed registrations, successful sign-ins, failed sign-ins, number of sign-ins per sec, etc. It may also have other metrics that possibly detects issues such as repeated failed logins with an email address.

Or, a payments service would have business metrics around successful/failed transactions, payment methods, autorenewals, etc.

For reference, here’s an [example SLO from Flipper](https://github.com/findmypast/flipper/blob/master/SLO.md).
