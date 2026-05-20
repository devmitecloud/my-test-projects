# EKS Upgrade Check Completion Guide

Use this guide with [README.md](README.md). The checklist tells you what must be true before an upgrade. This guide explains how to prove each item is complete. For execution-day steps, use [UPGRADE-RUNBOOK.md](UPGRADE-RUNBOOK.md).

## Recommended Tooling

- AWS CLI v2
- `kubectl`
- `eksctl` for EKS discovery and some node group operations
- `helm`
- `jq`
- `kubent` or `pluto` for deprecated API detection
- `velero` if you use it for cluster backup and restore

## Suggested Shell Variables

Set these before running the example commands:

```bash
export CLUSTER_NAME="your-cluster-name"
export AWS_REGION="eu-west-1"
export TARGET_VERSION="1.30"
```

## 1. Strategy and Change Readiness

### What to do

1. Confirm the cluster's current control plane version.
2. Confirm the exact target version and verify the version hop is supported by EKS.
3. Decide whether the upgrade is `in-place` or `blue-green`.
4. Write a rollback or failover plan that does not rely on control plane downgrade.
5. Define clear go/no-go criteria.
6. Get the change record, maintenance window, and owners approved.
7. Freeze unrelated deployments for the upgrade window.

### Useful commands

```bash
aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --query 'cluster.version' \
  --output text
```

### How to decide `in-place` vs `blue-green`

- Choose `in-place` when the cluster is healthy, API cleanup is small, and rolling node replacement is acceptable.
- Choose `blue-green` when rollback speed matters, the blast radius must be minimized, or you need major manifest/controller cleanup before cutover.

### Complete when

- Current version, target version, window, owners, and rollback or failover approach are documented.
- The change is approved.
- Everyone involved understands that EKS control plane downgrade is not supported.

## 2. Cluster Inventory

### What to do

1. Inventory all worker platforms in use.
2. Inventory all EKS-managed add-ons.
3. Inventory all controllers, operators, and Helm releases.
4. Inventory CRDs, webhooks, and stateful workloads.
5. Record current versions so you can compare them after the upgrade.

### Useful commands

```bash
aws eks list-nodegroups \
  --cluster-name "$CLUSTER_NAME" \
  --region "$AWS_REGION"

aws eks list-fargate-profiles \
  --cluster-name "$CLUSTER_NAME" \
  --region "$AWS_REGION"

aws eks list-addons \
  --cluster-name "$CLUSTER_NAME" \
  --region "$AWS_REGION"

kubectl get nodes -o wide
helm list -A
kubectl get crds
kubectl get validatingwebhookconfigurations,mutatingwebhookconfigurations
kubectl get statefulsets -A
kubectl get pvc,pv -A
```

### Extra checks

- If you use Karpenter, also inventory `NodePool`, `EC2NodeClass`, and `NodeClaim` objects.
- If you use self-managed nodes, capture launch template IDs, AMI IDs, and autoscaling group names.
- If you use custom AMIs, record how bootstrap is done.

### Complete when

- You have a current inventory of nodes, add-ons, controllers, CRDs, webhooks, and stateful services.
- You can identify every component that may need compatibility validation or a post-upgrade check.

## 3. Compatibility Validation

### What to do

1. Review the AWS EKS release notes for the target version.
2. Review Kubernetes deprecations and removals for the target version.
3. Check each add-on, controller, and operator for target-version support.
4. Check worker node AMI and OS support for the target version.
5. Check IRSA or Pod Identity dependencies and IAM permissions.

### Useful commands

```bash
aws eks describe-addon-versions \
  --addon-name vpc-cni \
  --kubernetes-version "$TARGET_VERSION" \
  --region "$AWS_REGION"

aws eks describe-addon-versions \
  --addon-name coredns \
  --kubernetes-version "$TARGET_VERSION" \
  --region "$AWS_REGION"

aws eks describe-addon-versions \
  --addon-name kube-proxy \
  --kubernetes-version "$TARGET_VERSION" \
  --region "$AWS_REGION"

aws eks list-pod-identity-associations \
  --cluster-name "$CLUSTER_NAME" \
  --region "$AWS_REGION"

kubectl get serviceaccounts -A \
  -o jsonpath='{range .items[*]}{.metadata.namespace}{"/"}{.metadata.name}{"  "}{.metadata.annotations.eks\.amazonaws\.com/role-arn}{"\n"}{end}'
```

### What to review manually

- AWS Load Balancer Controller release notes
- Karpenter or Cluster Autoscaler compatibility matrix
- `external-dns`, `cert-manager`, `metrics-server`, service mesh, logging, security, and policy agent release notes
- AMI support for AL2, AL2023, Bottlerocket, GPU nodes, and custom AMIs
- Any node bootstrap script that depends on version-specific kubelet flags

### Complete when

- Every add-on and platform component has a target-version-compatible release identified.
- Every node platform has a supported AMI and bootstrap method.
- No controller or IAM dependency is left unverified.

## 4. API Deprecation and Breaking Change Review

### What to do

1. Scan the live cluster for deprecated or removed APIs.
2. Scan repository manifests and Helm charts as well.
3. Upgrade or replace resources that use APIs removed in the target version.
4. Recheck after every remediation.

### Useful commands

```bash
kubent
pluto detect-all-in-cluster
pluto detect-files -d .

kubectl get ingress,hpa,pdb -A -o yaml
kubectl get crd -o yaml
kubectl get validatingwebhookconfigurations,mutatingwebhookconfigurations -o yaml
```

### What to pay attention to

- Old beta APIs
- Ingress API versions
- HPA API versions
- PodDisruptionBudget API versions
- CRD API versions
- Webhook API versions
- PodSecurityPolicy dependencies on older upgrade paths
- Helm charts that render removed APIs only at deploy time

### Complete when

- No live resource or rendered manifest uses an API removed in the target version.
- All deprecated API findings are either remediated or documented as false positives.

## 5. Pre-Upgrade Health Validation

### What to do

1. Confirm the cluster is healthy before starting.
2. Confirm system components are stable.
3. Confirm there is enough spare capacity for node replacement.
4. Confirm PodDisruptionBudgets will not block drains.
5. Confirm AWS quotas, ENIs, and subnet IPs are sufficient.

### Useful commands

```bash
kubectl get nodes
kubectl get pods -A
kubectl get events -A --sort-by=.lastTimestamp
kubectl get pdb -A
kubectl top nodes
kubectl top pods -A

aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --query 'cluster.resourcesVpcConfig.subnetIds' \
  --output text
```

### Practical checks

- Review `kube-system` carefully. Do not start if `vpc-cni`, `CoreDNS`, `kube-proxy`, CSI drivers, or admission controllers are already unhealthy.
- Test node drain behavior against at least one representative node.
- Review autoscaling limits for managed node groups, self-managed node groups, and Karpenter.
- Check subnet free IPs in the cluster subnets.
- Check relevant EC2, EBS, and load balancer quotas in AWS Service Quotas.

### Example drain dry run

```bash
kubectl drain <node-name> \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --dry-run=client
```

### Complete when

- All nodes are ready.
- There are no unresolved cluster-critical failures.
- You can rotate worker nodes without exhausting capacity or getting blocked by PDBs.

## 6. Backup and Recovery Readiness

### What to do

1. Confirm infrastructure source of truth is current.
2. Capture current cluster configuration and add-on versions.
3. Back up Helm values and important Kubernetes resources.
4. Back up all stateful data stores.
5. Test the restore process in a safe environment.

### Useful commands

```bash
aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION"

aws eks list-addons \
  --cluster-name "$CLUSTER_NAME" \
  --region "$AWS_REGION"

helm list -A
kubectl get crds -o yaml
kubectl get validatingwebhookconfigurations,mutatingwebhookconfigurations -o yaml
kubectl get storageclass
kubectl get pvc,pv -A
```

### Backup guidance

- Do not rely on `kubectl get all -A` alone. It does not cover every resource type.
- If you use Helm, export release values for every critical release.
- If you use Velero, create a backup and validate that a restore actually works.
- For data services, confirm EBS, EFS, RDS, and any external database backup policies are current.
- Record exactly where backups live and who can restore them.

### Complete when

- Configuration backup is complete.
- Stateful backups are confirmed.
- Restore steps were tested and produced a successful result.

## 7. Non-Production Rehearsal

### What to do

1. Rehearse the same version hop in a lower environment.
2. Use the same tooling and the same upgrade order you plan to use in production.
3. Run application smoke tests and platform validation after each phase.
4. Record issues, timing, and remediation steps.

### What to validate

- Ingress and load balancer behavior
- DNS updates and name resolution
- Storage attach, mount, and persistence behavior
- Node provisioning and autoscaling
- Service mesh behavior, if used
- Monitoring, logging, and alerts
- Business-critical application paths

### Complete when

- The rehearsal completed successfully.
- Any issue found in rehearsal is fixed or explicitly accepted before production.
- You have realistic timings for the production maintenance window.

## 8. Upgrade Sequence Prepared

### What to do

1. Write the exact command sequence before the maintenance window.
2. Define a validation checkpoint after each phase.
3. Prepare the node rotation procedure for each worker type.
4. Prepare the post-upgrade validation commands and dashboards.

### Typical execution order

1. Upgrade the EKS control plane.
2. Upgrade EKS-managed add-ons.
3. Upgrade worker nodes.
4. Upgrade dependent controllers and operators if needed.
5. Run workload and platform validation.

### Example commands

```bash
aws eks update-cluster-version \
  --name "$CLUSTER_NAME" \
  --kubernetes-version "$TARGET_VERSION" \
  --region "$AWS_REGION"

aws eks update-addon \
  --cluster-name "$CLUSTER_NAME" \
  --addon-name vpc-cni \
  --addon-version <target-addon-version> \
  --region "$AWS_REGION"

aws eks update-nodegroup-version \
  --cluster-name "$CLUSTER_NAME" \
  --nodegroup-name <nodegroup-name> \
  --region "$AWS_REGION"
```

### Notes

- If you use self-managed nodes, update the launch template or AMI and roll the autoscaling group in a controlled way.
- If you use Karpenter, verify both the controller version and the EC2 provisioning configuration are compatible before rotating nodes.
- Do not improvise during the production window. Pre-stage the commands and expected validation results.

### Complete when

- The run order is written down.
- Every phase has a validation gate.
- The owners for each phase are clear.

## 9. Operations and Communications

### What to do

1. Notify application owners and on-call teams.
2. Pause unrelated CI/CD pipelines and releases.
3. Prepare dashboards, logs, and alerts.
4. Create a live coordination channel for the upgrade window.
5. Define the escalation path if the upgrade must pause.

### What to have ready

- Cluster health dashboard
- Node readiness and scheduling dashboard
- Application error rate and latency dashboard
- Load balancer 4xx/5xx visibility
- Logging and audit trail access
- Contact list for platform, application, database, and security owners

### Complete when

- Everyone who must respond during the upgrade knows when and where to engage.
- Monitoring and alerting are already open before the first change is made.

## 10. Hard Stop Conditions

### What to do

Review every hard-stop item in [README.md](README.md). If any item is false, stop and remediate before production.

### Typical hard stops

- Deprecated APIs still in use
- Incompatible add-ons or controllers
- No tested restore path
- Not enough node replacement capacity
- PodDisruptionBudgets that block required drains
- No realistic rollback or failover procedure

### Complete when

- Every hard-stop item is explicitly true.
- Any exception has a documented risk owner and business approval.

## Go / No-Go Signoff

### Recommended reviewers

- Platform or infrastructure owner
- Application owner for critical workloads
- On-call lead
- Security or compliance approver if required by change policy

### What to confirm in the final review

1. The cluster is healthy right now.
2. The target version is supported by every critical component.
3. The rollback or failover plan is realistic.
4. Rehearsal completed successfully.
5. Monitoring and responders are ready.

### Complete when

- The final `go` decision is recorded in the change record or incident channel.

## Recommended Evidence to Save

Keep these with the change record:

- Current and target versions
- Inventory output for nodes, add-ons, and controllers
- Deprecated API scan results
- Health check outputs
- Backup and restore evidence
- Rehearsal notes and timings
- Final approved command sequence
- Go/no-go signoff record
