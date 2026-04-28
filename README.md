# success-devops

Production-grade DevOps on Microsoft Azure -- two microservices applications built end-to-end with Infrastructure as Code, Kubernetes, CI/CD, and observability.

## Why this repo exists

This is a hands-on portfolio of cloud engineering skills, built across 25 progressive classes covering everything a modern DevOps / SRE / Platform engineer needs:

- Containers (Docker, distroless, image scanning, signing)
- Container orchestration (AKS, Kubernetes manifests, Helm, Kustomize)
- Infrastructure as Code (Terraform with remote state, modules, multi-env)
- CI/CD (Azure DevOps pipelines, multi-stage, blue-green, GitOps with ArgoCD)
- Networking (VNets, Private Endpoints, NGINX Ingress, cert-manager)
- Security (Workload Identity, Key Vault CSI, Network Policies, RBAC)
- Observability (App Insights, Log Analytics, Prometheus, Grafana)
- Reliability (HPA, KEDA, PodDisruptionBudgets, Chaos engineering)

## Applications

### `app-01-shopwave/` -- ShopWave (mini Amazon)
A 6-service e-commerce platform: frontend, catalog, cart, orders, payments worker, notifier function.

- 6 Python microservices
- Postgres Flexible Server, Service Bus, Key Vault, ACR, AKS, NGINX Ingress
- Workload Identity Federation (no client secrets)
- Multi-stage CI/CD pipeline with blue-green deploy
- Full observability: SLOs, alerts, distributed tracing

### `app-02-streamhub/` -- StreamHub (mini Netflix)
A video streaming platform with Cosmos DB, Event Hub, transcoder workers, ML-driven recommendations, Azure AD B2C auth.

Built solo to prove mastery of the patterns learned in App 1.

## Repository structure

```
.
|-- app-01-shopwave/
|   |-- docs/                   architecture, ADRs
|   |-- services/               6 Python services
|   |-- infra/                  Terraform modules + envs
|   |-- k8s/                    Kustomize base + overlays
|   |-- pipelines/              Azure DevOps YAML
|-- app-02-streamhub/           same structure as App 1
|-- _class-notes/               per-class learning notes
|-- README.md                   you are here
|-- .gitignore
```

## Branching strategy

Trunk-based development. `main` is always deployable. All work happens in short-lived feature branches that must pass CI checks and require 1 approval before squash-merging.

## Cost discipline

All resources are tagged with `Project=shopwave|streamhub`, `Env=dev`, `CostCenter=learning`. A subscription budget alerts at 50% / 80% / 100% of the monthly cap. Long-running resources are stopped at end of every working session.

## License

MIT
