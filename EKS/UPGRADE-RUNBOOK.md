# EKS Upgrade Runbook

Use this runbook for the execution window after all items in [README.md](README.md) are complete.

## Purpose

This document is the operational procedure for performing an EKS upgrade in a controlled way. It is intended for use during the maintenance window and should be completed together with live monitoring, incident coordination, and change tracking.

## Scope

This runbook covers:

- control plane upgrade
- EKS managed add-on upgrades
- worker node upgrades
- controller validation
- workload validation
- pause, rollback, and failover decision points

This runbook does not replace the pre-upgrade checklist. Do not start until [README.md](README.md) is complete.

## Roles

- Upgrade lead: owns execution and go/no-go calls during the window
- Platform operator: runs the upgrade commands
- Application validator: confirms application health and smoke tests
- Observer or incident lead: watches alerts, dashboards, and escalation path

## Recommended Shell Variables

Set these before the window starts:

```bash
export CLUSTER_NAME="your-cluster-name"
export AWS_REGION="eu-west-1"
export TARGET_VERSION="1.30"
```

Optional variables:

```bash
export NODEGROUP_NAME="your-nodegroup"
export ADDON_NAME="vpc-cni"
```

## Execution Record

- Change record / ticket: `________________________`
- Maintenance window start: `________________________`
- Maintenance window end: `________________________`
- Upgrade lead: `________________________`
- Platform operator: `________________________`
- Application validator: `________________________`
- Observer / incident lead: `________________________`

## 1. Pre-Flight Gate

Do not execute any upgrade command until these are true.

- [ ] All items in [README.md](README.md) are complete.
- [ ] Monitoring dashboards are open.
- [ ] Alerts are reviewed and understood.
- [ ] Incident or coordination channel is active.
- [ ] Rollback or failover owner is online.
- [ ] Application owners are online or on standby.
- [ ] Current cluster health is green.
- [ ] Current control plane version confirmed.
- [ ] Current add-on versions confirmed.
- [ ] Current node group versions confirmed.

### Baseline Commands

Run and save the outputs before the first change:

```bash
aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION"

aws eks list-addons \
  --cluster-name "$CLUSTER_NAME" \
  --region "$AWS_REGION"

kubectl get nodes -o wide
kubectl get pods -A
kubectl get pdb -A
helm list -A
```

### Hold Point

Pause here if any critical workload is unhealthy, any alert is already firing for cluster stability, or the maintenance window no longer has enough time.

## 2. Control Plane Upgrade

### Objective

Upgrade the EKS control plane by one supported minor version.

### Command

```bash
aws eks update-cluster-version \
  --name "$CLUSTER_NAME" \
  --kubernetes-version "$TARGET_VERSION" \
  --region "$AWS_REGION"
```

### Watch Progress

```bash
aws eks describe-update \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --update-id <update-id>

aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --query 'cluster.version' \
  --output text
```

### Validation Checks

- [ ] Control plane update completed successfully.
- [ ] API server reachable through `kubectl`.
- [ ] `kubectl get nodes` succeeds.
- [ ] `kubectl get pods -A` succeeds.
- [ ] No new critical failures in `kube-system`.
- [ ] Admission webhooks are functioning.

### Hold Point

Do not continue if:

- API server access is unstable
- `kube-system` has critical failures
- cluster networking is degraded
- admission controllers are blocking workloads unexpectedly

### If Failed

- Stop the runbook.
- Open or update the incident channel.
- Engage AWS Support if the failure is in the managed control plane.
- Execute the failover plan if business impact requires it.

## 3. Managed Add-On Upgrades

### Objective

Upgrade EKS managed add-ons to versions compatible with the target control plane version.

### Typical Add-Ons

- `vpc-cni`
- `coredns`
- `kube-proxy`
- `aws-ebs-csi-driver` if managed by EKS

### Discover Compatible Versions

```bash
aws eks describe-addon-versions \
  --addon-name "$ADDON_NAME" \
  --kubernetes-version "$TARGET_VERSION" \
  --region "$AWS_REGION"
```

### Example Upgrade Command

```bash
aws eks update-addon \
  --cluster-name "$CLUSTER_NAME" \
  --addon-name "$ADDON_NAME" \
  --addon-version <target-addon-version> \
  --region "$AWS_REGION"
```

### Validation Checks

Run these checks after each add-on, not only at the end.

- [ ] Add-on update completed successfully.
- [ ] Add-on pods are healthy.
- [ ] `kube-system` remains stable.
- [ ] DNS resolution works after `CoreDNS` upgrade.
- [ ] Pod networking works after `vpc-cni` upgrade.
- [ ] Node to API communication works after `kube-proxy` upgrade.
- [ ] Volume provisioning and attachment works after CSI driver upgrade.

### Useful Commands

```bash
kubectl get pods -n kube-system
kubectl get ds -n kube-system
kubectl get deploy -n kube-system
kubectl get csinodes
kubectl get storageclass
```

### Hold Point

Do not continue if DNS, pod networking, storage attachment, or node networking is degraded.

## 4. Worker Node Upgrade

### Objective

Move worker nodes to versions and AMIs compatible with the new control plane.

Choose the section that matches your node model.

## 4A. Managed Node Groups

### Example Command

```bash
aws eks update-nodegroup-version \
  --cluster-name "$CLUSTER_NAME" \
  --nodegroup-name "$NODEGROUP_NAME" \
  --region "$AWS_REGION"
```

If using a launch template, ensure the template version is already updated to the intended AMI and bootstrap configuration before starting node rotation.

### Validation Checks

- [ ] New nodes join successfully.
- [ ] New nodes report `Ready`.
- [ ] Old nodes drain cleanly.
- [ ] No workload remains stuck in `Pending`.
- [ ] No PDB blocks the rollout.
- [ ] Critical workloads remain available.

### Useful Commands

```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get pdb -A
kubectl get events -A --sort-by=.lastTimestamp
```

## 4B. Self-Managed Nodes

### Procedure

1. Update the launch template or node AMI.
2. Increase desired capacity if surge nodes are required.
3. Allow new nodes to join and become ready.
4. Cordon and drain old nodes in batches.
5. Remove old nodes from the autoscaling group after workloads are stable.

### Example Drain Command

```bash
kubectl drain <node-name> \
  --ignore-daemonsets \
  --delete-emptydir-data
```

### Validation Checks

- [ ] Replacement nodes joined successfully.
- [ ] Workloads rescheduled successfully.
- [ ] No storage or network regressions observed.
- [ ] Old nodes removed cleanly.

## 4C. Karpenter-Managed Nodes

### Procedure

1. Confirm the Karpenter controller version supports the target cluster version.
2. Confirm `NodePool`, `EC2NodeClass`, and instance profile configuration are valid.
3. Trigger controlled node replacement using your approved process.
4. Watch provisioning, scheduling, and node termination closely.

### Validation Checks

- [ ] Karpenter provisions replacement nodes successfully.
- [ ] Replacement nodes are ready and schedulable.
- [ ] Consolidation or disruption logic does not evict critical workloads unexpectedly.
- [ ] No scale-up failures from IAM, subnet, or quota constraints.

## 4D. Fargate Workloads

### Procedure

1. Confirm the Fargate profile configuration is unchanged and valid.
2. Recycle representative workloads if needed to confirm scheduling behavior.
3. Validate DNS, networking, and IAM behavior for Fargate-backed pods.

### Validation Checks

- [ ] Fargate-backed pods schedule successfully.
- [ ] Pod startup and networking are normal.
- [ ] Application traffic is healthy.

### Hold Point For All Worker Types

Do not continue if:

- replacement nodes fail to join
- workloads cannot reschedule
- cluster capacity becomes constrained
- storage mounts fail
- application health degrades beyond agreed thresholds

## 5. Controller and Platform Validation

### Objective

Validate all non-EKS platform controllers after the control plane and workers are upgraded.

### Components to Check

- AWS Load Balancer Controller
- Cluster Autoscaler or Karpenter
- `external-dns`
- `cert-manager`
- `metrics-server`
- service mesh
- logging agents
- security agents
- policy engines

### Useful Commands

```bash
kubectl get pods -A
kubectl get deploy -A
kubectl get validatingwebhookconfigurations,mutatingwebhookconfigurations
helm list -A
```

### Validation Checks

- [ ] No controller is crash-looping.
- [ ] No webhook is rejecting valid workloads unexpectedly.
- [ ] Ingress or load balancer reconciliation works.
- [ ] DNS reconciliation works.
- [ ] Certificate issuance or renewal path works.
- [ ] Metrics collection works.
- [ ] Autoscaling logic works.
- [ ] Logging and security telemetry works.

### Hold Point

Pause here if any controller is unhealthy or if a webhook failure affects workload creation, scaling, or ingress.

## 6. Application Validation

### Objective

Prove that business-critical applications function normally after the platform upgrade.

### Minimum Checks

- [ ] Critical applications are running.
- [ ] Critical application pods are ready.
- [ ] External traffic reaches the correct services.
- [ ] Internal service-to-service traffic is healthy.
- [ ] Background jobs, workers, and queues are healthy.
- [ ] Persistent workloads can read and write data.
- [ ] Smoke tests passed.
- [ ] Error rates and latency remain within agreed thresholds.

### Suggested Commands

```bash
kubectl get deploy,statefulset,daemonset -A
kubectl get svc,ingress -A
kubectl get pods -A
kubectl logs -n <namespace> <pod-name> --tail=100
```

### Hold Point

Do not close the change if critical business paths have not been validated.

## 7. Post-Upgrade Final Verification

### Objective

Confirm the cluster is fully upgraded and stable.

### Checks

- [ ] Cluster control plane version matches the target version.
- [ ] Add-on versions match the intended versions.
- [ ] Worker nodes are on the intended Kubernetes and AMI versions.
- [ ] Old worker nodes have been removed.
- [ ] Cluster capacity is stable.
- [ ] No unexpected alerts remain active.
- [ ] Audit, logging, and monitoring are healthy.
- [ ] Final smoke tests passed.

### Example Commands

```bash
aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --query 'cluster.version' \
  --output text

aws eks describe-nodegroup \
  --cluster-name "$CLUSTER_NAME" \
  --nodegroup-name "$NODEGROUP_NAME" \
  --region "$AWS_REGION"

kubectl version
kubectl get nodes -o wide
kubectl get pods -A
```

## 8. Pause, Rollback, and Failover Guidance

### Important Constraint

EKS control plane downgrade is not supported. If the control plane is already upgraded, rollback normally means workload failback, traffic cutback, or business failover to another environment, not version downgrade.

### Pause the Upgrade When

- core cluster services become unstable
- workload availability drops below the agreed threshold
- DNS, ingress, or storage is degraded
- node replacement is blocked and capacity is at risk
- monitoring visibility is lost

### Roll Back When

- the issue is isolated to a change that can be safely reversed without downgrading the control plane
- for example, an add-on version, controller release, launch template, or application release introduced during the window

### Fail Over When

- business impact exceeds the allowed threshold
- platform stability cannot be restored in the maintenance window
- the pre-approved blue-green or disaster recovery target is ready to receive traffic

### Minimum Actions During a Pause or Incident

1. Stop further change execution.
2. Record the exact failure point.
3. Preserve logs, command output, and dashboards.
4. Notify stakeholders and incident responders.
5. Decide between restore, rollback of reversible components, or failover.

## 9. Closeout

### Before Ending the Window

- [ ] Final validation completed.
- [ ] Stakeholders informed of outcome.
- [ ] Incident channel updated or closed.
- [ ] Change record updated.
- [ ] Follow-up tasks documented.
- [ ] Any deferred remediation captured with owners and due dates.

### Record

- Upgrade outcome: `successful / partial / failed`
- End time: `________________________`
- Incident reference: `________________________`
- Follow-up actions: `________________________`

## 10. Evidence to Retain

Save these artifacts with the change record:

- command history used during the run
- before and after cluster version output
- before and after node inventory
- add-on upgrade results
- screenshots or exports of monitoring state
- smoke test results
- incident notes and decisions if any pause occurred
