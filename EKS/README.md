# EKS Upgrade Prerequisites

Before upgrading an EKS cluster, treat these as mandatory prerequisites:

## 1. Define the upgrade strategy

- Confirm the current Kubernetes/EKS version, target version, and supported hop sequence. EKS upgrades should be done one minor version at a time.
- Decide whether the upgrade is `in-place` or `blue/green`.
- Plan rollback correctly: EKS control plane downgrade is not supported, so rollback means failover to another cluster or restore/redeploy, not version rollback.
- Set a maintenance window, change freeze, owners, and clear go/no-go criteria.

## 2. Inventory the full cluster

- Identify all node types: managed node groups, self-managed nodes, Karpenter, Fargate.
- Inventory core add-ons: `vpc-cni`, `CoreDNS`, `kube-proxy`, `EBS CSI`, `EFS CSI`.
- Inventory platform controllers: AWS Load Balancer Controller, Cluster Autoscaler or Karpenter, `external-dns`, `cert-manager`, `metrics-server`, service mesh, logging/monitoring agents, security agents.
- Identify all CRDs, operators, admission webhooks, and stateful workloads.

## 3. Build a compatibility matrix

- Review AWS EKS release notes for the target version.
- Review upstream Kubernetes API deprecations and removals for that version.
- Verify every add-on/controller supports the target cluster version.
- Verify AMI/OS compatibility for worker nodes, including custom AMIs, Bottlerocket, AL2/AL2023, GPU/device plugins, and bootstrap method.
- Check IRSA/Pod Identity and IAM permissions required by upgraded components.

## 4. Scan for breaking API usage

- Check for deprecated or removed Kubernetes APIs with tools like `kubent` or `pluto`.
- Pay special attention to:
- old beta APIs
- CRDs and webhooks
- ingress resources
- PDBs
- HPA versions
- PodSecurityPolicy removal on older upgrade paths
- Confirm Helm charts and operators use APIs supported by the target version.

## 5. Validate cluster health before touching it

- All nodes should be `Ready`.
- No failing system pods in `kube-system`.
- No unresolved incidents, high error rates, or persistent `CrashLoopBackOff` / `Pending` pods.
- Review PodDisruptionBudgets and drain behavior so worker replacement does not stall.
- Confirm enough spare capacity for rolling node upgrades.
- Check EC2 quotas, subnet free IPs, ENI limits, and autoscaling headroom.

## 6. Back up and verify recovery

- Back up cluster resources and workload state.
- For stateful apps, ensure EBS/EFS/RDS snapshots or equivalent backups exist.
- Save current add-on versions, Helm values, launch template versions, and IaC state.
- Test restore procedures. A backup without a restore test is not enough.

## 7. Rehearse in non-production

- Run the same upgrade path in staging or a like-for-like lower environment.
- Validate ingress, DNS, storage, autoscaling, service mesh, monitoring, and application smoke tests.
- Capture pre-upgrade baselines so regressions are easy to spot.

## 8. Prepare the upgrade order

- Upgrade the EKS control plane first.
- Upgrade EKS managed add-ons next.
- Upgrade worker nodes after that.
- Then upgrade dependent controllers and validate workloads.
- Use checkpoints between each phase before proceeding.

## 9. Prepare operations and communications

- Notify application owners and on-call teams.
- Freeze unrelated deployments during the upgrade window.
- Ensure dashboards, logs, alerts, and responders are ready before starting.

## Hard blockers I would not ignore

- Deprecated APIs still in use
- Add-ons/controllers not compatible with the target version
- No tested restore path
- No spare capacity for node rotation
- PDBs that block node drains
- No realistic rollback/failover plan
