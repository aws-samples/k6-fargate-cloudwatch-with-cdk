# K6 Fargate with CloudWatch on AWS

## Introduction
This sample project provides an easy way to run load test with a K6 container in an ECS Fargate Task.
The metrics are collected by the CloudWatch Agent sidecar in the Fargate Task. 
This project also provides a CloudWatch Dashboard to view the load testing result in the CloudWatch.

## Architecture Diagram
![Architecture](img/k6-fargate.png?raw=true "Architecture")
## Requirements
* Python3
* CDK
## Setup
### pip install
```
$ pip install -r requirements.txt
```

## Deploy 
To get start it is just need to simply deploy the stack with the command "cdk deploy". 
```
cdk deploy
```

## Run Load Test
An ECS Cluster and a Task Definition will deploy by the CloudFormation
Access the AWS Console find the ECS Cluster 
Run a new task using the ECS Task Definition.

![Run Fargate Task](img/run_fargate_task.png?raw=true "Run Fargate Task")

## Monitoring
This sample also include a CloudWatch Dashboard to simply monitoring the metrics for the load test.


### Create CloudWatch Dashboard
Replace all the region code in the CloudWatch dashboard template "cloudwatch-metrics-dashboard/dashboard.json".

![Replace Region](img/replace_region.png?raw=true "Replace Region")

Create a new CloudWatch Dashboard in the AWS Console. 

Then open the dashboard, select "Action -> View/edit source" paste the template.

![Edit CloudWatch Dashboard](img/edit_dashboard.png?raw=true "Edit CloudWatch Dashboard")

After creating the dashboard, you can monitor the load tests with CloudWatch dashboard.

![CloudWatch Dashboard](img/cloudwatch_dashboard.png?raw=true "CloudWatch Dashboard")

## References
* https://k6.io/docs/results-visualization/amazon-cloudwatch/
* https://github.com/aws/amazon-cloudwatch-agent/blob/master/amazon-cloudwatch-container-insights/ecs-task-definition-templates/deployment-mode/sidecar/cwagent-emf/README.md
* https://github.com/grafana/k6-example-cloudwatch-dashboards

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

