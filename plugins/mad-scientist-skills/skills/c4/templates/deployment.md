# Deployment Diagram Template (C4 Supplementary) — Structurizr DSL

Shows **where containers run** in the real infrastructure: cloud regions, clusters, servers, CDNs, and network boundaries. This is the diagram you use for infrastructure reviews, cloud cost discussions, disaster recovery planning, and DevOps onboarding.

## Purpose

Answer: "Where does everything actually run? What infrastructure hosts our containers?"

## Architect's checklist

Before building this diagram, identify:

- [ ] **Deployment environment** — Production? Staging? Dev? (one diagram per environment, or one with environment switching)
- [ ] **Cloud provider(s)** — AWS, Azure, GCP, on-prem, hybrid?
- [ ] **Regions and zones** — Where are things deployed geographically?
- [ ] **Compute nodes** — VMs, containers, serverless, managed services
- [ ] **Networking** — Load balancers, CDNs, VPNs, firewalls, VPCs
- [ ] **Data stores** — Managed databases, self-hosted DBs, object storage
- [ ] **Scaling** — How many instances? Auto-scaling groups?
- [ ] **Security boundaries** — Public subnet, private subnet, VPC, trust zones

## Layout

```
+--------------------------------------------------+
|  Tab bar: [Context] [Container] ... [Deployment*] |
+--------------------------------------------------+
|                                                    |
|  +-- AWS Region: us-east-1 -------------------+   |
|  |                                             |   |
|  |  +-- Public Subnet ----------+              |   |
|  |  |  +------+  +----------+  |              |   |
|  |  |  | CDN  |  | ALB      |  |              |   |
|  |  |  +------+  +----------+  |              |   |
|  |  +---------------------------+              |   |
|  |                                             |   |
|  |  +-- Private Subnet ---------+              |   |
|  |  |  +----------+ +--------+  |              |   |
|  |  |  | ECS Task | | ECS    |  |              |   |
|  |  |  | API x3   | | Worker |  |              |   |
|  |  |  +----------+ +--------+  |              |   |
|  |  +---------------------------+              |   |
|  |                                             |   |
|  |  +-- Data Subnet ------------+              |   |
|  |  |  +------+ +-----+ +----+ |              |   |
|  |  |  | RDS  | |Redis| | SQS| |              |   |
|  |  |  +------+ +-----+ +----+ |              |   |
|  |  +---------------------------+              |   |
|  +---------------------------------------------+  |
|                                                    |
+--------------------------------------------------+
|  Structurizr DSL Source                    [Copy]  |
+--------------------------------------------------+
```

## Structurizr DSL syntax for this level

```
workspace "System Name" "Deployment diagram" {

    model {
        system = softwareSystem "System Name" "Core system" {
            spa = container "Web App" "Static SPA assets served globally" "React"
            api = container "API Service" "Handles business logic" "Node.js 20, Express"
            worker = container "Background Worker" "Processes async jobs" "Node.js 20, Bull"
            db = container "Database" "Primary + standby replica" "PostgreSQL 15" "Database"
            cache = container "Cache" "2-node cluster" "Redis 7" "Database"
            queue = container "Job Queue" "Durable message queue" "SQS FIFO" "Queue"
        }

        production = deploymentEnvironment "Production" {
            deploymentNode "CloudFront CDN" "Global edge distribution" "AWS CloudFront" {
                containerInstance spa
            }

            deploymentNode "AWS" "Amazon Web Services" "Cloud" {
                deploymentNode "us-east-1" "US East" "AWS Region" {

                    deploymentNode "Public Subnet" "Internet-facing" "VPC" {
                        infrastructureNode "Load Balancer" "Routes traffic, terminates TLS" "AWS ALB"
                    }

                    deploymentNode "Private Subnet" "Internal only" "VPC" {
                        deploymentNode "ECS Cluster" "Container orchestration" "AWS Fargate" {
                            deploymentNode "API Task Definition" "x3 instances, auto-scaling" "" {
                                containerInstance api
                            }
                            deploymentNode "Worker Task Definition" "x2 instances" "" {
                                containerInstance worker
                            }
                        }
                    }

                    deploymentNode "Data Subnet" "No public access" "VPC" {
                        deploymentNode "RDS" "Multi-AZ" "AWS Managed" {
                            containerInstance db
                        }
                        deploymentNode "ElastiCache" "Cluster mode" "AWS Managed" {
                            containerInstance cache
                        }
                    }

                    deploymentNode "SQS" "Managed queue service" "AWS Managed" {
                        containerInstance queue
                    }
                }
            }
        }
    }

    views {
        deployment system "Production" "Deployment_Production" {
            include *
            autoLayout
        }

        styles {
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "Database" {
                shape Cylinder
            }
            element "Queue" {
                shape Pipe
            }
            element "Infrastructure Node" {
                background #ffffff
                color #000000
            }
        }
    }

}
```

## Best practices for Deployment diagrams

| Practice | Why |
|----------|-----|
| **One environment per diagram** | Production and staging have different topologies. Use separate deployment views. |
| **Nest deployment nodes** | Cloud -> Region -> VPC -> Subnet -> Cluster -> Task. Nesting shows the actual hierarchy. |
| **Specify instance counts** | "x3 instances, auto-scaling" in the deployment node description |
| **Include network boundaries** | Public vs. private subnet, VPC, security groups — these define access patterns |
| **Show managed services explicitly** | RDS, ElastiCache, SQS are deployment nodes. The container instance runs inside them. |
| **Use infrastructureNode for non-container infra** | Load balancers, CDNs, firewalls — things that aren't your containers |
| **Map containers from Level 2** | Every container from your Container diagram should appear here as `containerInstance` |

## Deployment node hierarchy

```
Cloud Provider (AWS / Azure / GCP / On-Prem)
  +-- Region (us-east-1 / westeurope)
       +-- Availability Zone (us-east-1a) [optional — for HA diagrams]
            +-- VPC / Virtual Network
                 +-- Subnet (Public / Private / Data)
                      +-- Compute (ECS, EKS, EC2, Lambda, App Service)
                           +-- containerInstance (your app from Level 2)
```

## Cloud-specific deployment node examples

### AWS
| Node | Description |
|------|-------------|
| `AWS CloudFront` | CDN for static assets |
| `ALB` / `NLB` | Application / Network load balancer |
| `ECS Fargate` | Serverless container orchestration |
| `EKS` | Managed Kubernetes |
| `RDS` | Managed relational database |
| `ElastiCache` | Managed Redis/Memcached |
| `SQS` / `SNS` | Queue / pub-sub |
| `S3` | Object storage |
| `Lambda` | Serverless functions |

### Azure
| Node | Description |
|------|-------------|
| `Azure Front Door` | Global load balancer + CDN |
| `App Service` | Managed web hosting |
| `AKS` | Managed Kubernetes |
| `Azure SQL` | Managed database |
| `Azure Cache for Redis` | Managed cache |
| `Service Bus` | Message queue |
| `Blob Storage` | Object storage |
| `Azure Functions` | Serverless compute |

### GCP
| Node | Description |
|------|-------------|
| `Cloud CDN` | Content delivery |
| `Cloud Run` | Serverless containers |
| `GKE` | Managed Kubernetes |
| `Cloud SQL` | Managed database |
| `Memorystore` | Managed Redis |
| `Pub/Sub` | Messaging |
| `Cloud Storage` | Object storage |
| `Cloud Functions` | Serverless compute |

## Security boundary annotations

Use deployment node nesting to make security boundaries visible:

```
Public subnet (internet-facing)
  +-- Load balancer, CDN

Private subnet (internal only)
  +-- Application containers

Data subnet (no public route)
  +-- Databases, caches, queues
```

## Anti-patterns to avoid

- **Flat diagram** — No nesting. Just boxes floating with no infrastructure context. Always nest.
- **Missing the infrastructure** — Only showing containers without where they run defeats the purpose.
- **Combining environments** — Prod and staging in one diagram gets confusing fast. Use separate deployment views.
- **Forgetting replicas** — "x3 instances" matters for understanding scale and availability.
- **No network boundaries** — The difference between public and private subnet is a security fundamental.
- **Showing code-level details** — This is infrastructure. No classes, functions, or internal component wiring.
- **Missing containerInstance** — Deployment nodes without `containerInstance` references don't connect to the model. Always place containers.
