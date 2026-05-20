# EKS Upgrade Checklist

Use this checklist as a reusable pre-upgrade procedure for Amazon EKS cluster upgrades.

Detailed completion guidance for each checklist section is in [README-CHECK-GUIDE.md](README-CHECK-GUIDE.md).
Execution-day steps are in [UPGRADE-RUNBOOK.md](UPGRADE-RUNBOOK.md).

## Core Upgrade Rules

- [ ] Track EKS release cadence and support windows. New Kubernetes and EKS minor versions are typically released about every 14 weeks, so upgrades should be planned before support deadlines.
- [ ] Confirm the upgrade path is incremental only: one minor version at a time.
- [ ] If crossing multiple minor versions, document every intermediate hop in the path, for example `1.31 -> 1.32 -> 1.33 -> 1.34`.
- [ ] Confirm the EKS control plane cannot be downgraded once upgraded.
- [ ] Confirm the control plane will be upgraded before any add-ons or worker nodes.
- [ ] Confirm add-ons and worker nodes will only be upgraded after the control plane; after that, they may be upgraded in either order if compatibility allows.
- [ ] Confirm worker nodes are never newer than the control plane.
- [ ] Confirm worker nodes are either the same version as the control plane or no more than two minor versions lower.

## Upgrade Metadata

- [ ] Cluster name: `________________________`
- [ ] Environment: `dev / test / stage / prod`
- [ ] AWS account ID: `________________________`
- [ ] AWS region: `________________________`
- [ ] Current EKS version: `________________________`
- [ ] Target EKS version: `________________________`
- [ ] Upgrade type selected: `in-place / blue-green`
- [ ] Planned maintenance window: `________________________`
- [ ] Change record / ticket: `________________________`
- [ ] Primary owner: `________________________`
- [ ] Approver: `________________________`
- [ ] Rollback or failover owner: `________________________`

## 1. Strategy and Change Readiness

- [ ] Confirm the current Kubernetes/EKS version and exact target version.
- [ ] Confirm the upgrade path is supported by EKS.
- [ ] Confirm the upgrade will be performed one minor version at a time.
- [ ] Review release notes and changelogs for every Kubernetes or EKS version in the upgrade path, not only the final target version.
- [ ] Decide and document whether the upgrade is `in-place` or `blue-green`.
- [ ] Document the rollback strategy.
- [ ] Confirm stakeholders understand that EKS control plane downgrade is not supported.
- [ ] Define go/no-go criteria.
- [ ] Schedule and approve the maintenance window.
- [ ] Confirm the upgrade timing aligns with EKS support dates and release cadence.
- [ ] Freeze unrelated infrastructure and application changes during the upgrade window.

## 2. Cluster Inventory

- [ ] Inventory worker platform types in use.
- [ ] Managed node groups documented.
- [ ] Self-managed node groups documented.
- [ ] Karpenter usage documented.
- [ ] Fargate profiles documented.
- [ ] Current node AMIs and OS families documented.
- [ ] Core add-ons documented: `vpc-cni`, `CoreDNS`, `kube-proxy`.
- [ ] Storage drivers documented: `EBS CSI`, `EFS CSI`.
- [ ] Platform controllers documented: AWS Load Balancer Controller, Cluster Autoscaler or Karpenter, `external-dns`, `cert-manager`, `metrics-server`.
- [ ] Observability and security agents documented.
- [ ] Service mesh components documented, if used.
- [ ] All CRDs documented.
- [ ] All operators documented.
- [ ] All admission webhooks documented.
- [ ] Stateful workloads and storage dependencies documented.

## 3. Compatibility Validation

- [ ] Review AWS EKS release notes for the target version.
- [ ] Review upstream Kubernetes deprecations and removals for the target version.
- [ ] Confirm the current worker node versions are compliant with supported version skew before the upgrade starts.
- [ ] If your operating standard requires it, confirm the control plane version and worker node versions match at the start of the upgrade.
- [ ] Confirm all EKS managed add-ons support the target version.
- [ ] Confirm all Helm charts and controllers support the target version.
- [ ] Confirm CRDs are compatible with the target version.
- [ ] Confirm webhooks are compatible with the target version.
- [ ] Confirm AMI and OS compatibility for all worker node types.
- [ ] Confirm compatibility for AL2, AL2023, Bottlerocket, or custom AMIs as applicable.
- [ ] Confirm GPU workloads and device plugins are compatible, if used.
- [ ] Confirm bootstrap method compatibility for node provisioning.
- [ ] Confirm IRSA or Pod Identity dependencies remain valid after upgrade.
- [ ] Confirm IAM permissions required by upgraded add-ons and controllers.

## 4. API Deprecation and Breaking Change Review

- [ ] Run a deprecated API scan using `kubent`, `pluto`, or equivalent.
- [ ] Review findings for removed or deprecated beta APIs.
- [ ] Confirm all manifest files are updated for API changes identified in the reviewed release notes.
- [ ] Review Ingress API usage.
- [ ] Review HPA API usage.
- [ ] Review PodDisruptionBudget API usage.
- [ ] Review CRD API versions.
- [ ] Review webhook API versions.
- [ ] Confirm PodSecurityPolicy dependencies are removed where applicable.
- [ ] Confirm no application manifests rely on APIs removed in the target version.
- [ ] Confirm no Helm release templates render removed APIs for the target version.

## 5. Pre-Upgrade Health Validation

- [ ] Confirm all cluster nodes are `Ready`.
- [ ] Confirm no critical pods are failing in `kube-system`.
- [ ] Confirm there are no unresolved production incidents.
- [ ] Confirm there are no sustained `CrashLoopBackOff` workloads requiring remediation.
- [ ] Confirm there are no critical `Pending` pods caused by scheduling or capacity issues.
- [ ] Review PodDisruptionBudgets for drain safety.
- [ ] Confirm node draining can complete without violating workload availability requirements.
- [ ] Confirm autoscaling headroom exists for rolling node replacement.
- [ ] Confirm EC2 instance quotas are sufficient.
- [ ] Confirm subnet free IP capacity is sufficient.
- [ ] Confirm at least 5 free IP addresses are available in each subnet used for the rolling worker node upgrade.
- [ ] Confirm ENI/IP allocation capacity is sufficient.
- [ ] Confirm load balancer, volume, and other AWS service quotas are sufficient if relevant.

## 6. Backup and Recovery Readiness

- [ ] Back up cluster manifests, Helm values, and infrastructure configuration.
- [ ] Capture current versions of all add-ons and controllers.
- [ ] Capture current launch template versions or node configuration.
- [ ] Verify IaC source of truth is current and recoverable.
- [ ] If Kubernetes configuration is fully managed in Git or IaC, document that configuration recovery will come from source control; stateful data backups are still required.
- [ ] Confirm backups exist for all stateful services.
- [ ] Confirm EBS snapshots exist where required.
- [ ] Confirm EFS backup or recovery strategy exists where required.
- [ ] Confirm RDS or external data store backups exist where required.
- [ ] Test and document restore steps.
- [ ] Confirm restore validation was completed successfully.

## 7. Non-Production Rehearsal

- [ ] Rehearse the same upgrade path in a lower environment.
- [ ] Promote the change through lower environments first, for example `dev -> UAT -> prod`.
- [ ] Match production architecture closely enough for the rehearsal to be meaningful.
- [ ] Validate ingress after rehearsal.
- [ ] Validate DNS after rehearsal.
- [ ] Validate storage attachment and persistence after rehearsal.
- [ ] Validate autoscaling after rehearsal.
- [ ] Validate service mesh behavior after rehearsal, if used.
- [ ] Validate observability pipeline after rehearsal.
- [ ] Run application smoke tests after rehearsal.
- [ ] Record issues found in rehearsal and confirm they are resolved.
- [ ] Capture pre-upgrade and post-upgrade baseline metrics.

## 8. Upgrade Sequence Prepared

- [ ] Document the exact execution order.
- [ ] Control plane upgrade step prepared as the first mandatory phase.
- [ ] Confirm no add-on or worker node upgrade will start before the control plane upgrade completes.
- [ ] EKS managed add-on upgrade step prepared.
- [ ] Worker node upgrade step prepared.
- [ ] Confirm whether add-ons or worker nodes will be second and third in this run.
- [ ] Dependent controller upgrade step prepared.
- [ ] Validation checkpoint after each phase defined.
- [ ] Node rotation and drain procedure documented.
- [ ] Confirm the node rotation procedure includes cordon or unschedulable steps so no new pods are scheduled on nodes being replaced.
- [ ] Surge or spare capacity plan documented.
- [ ] Post-upgrade verification commands and dashboards prepared.

## 9. Operations and Communications

- [ ] Notify application owners.
- [ ] Notify on-call and incident response teams.
- [ ] Notify all other affected stakeholders.
- [ ] Confirm operator coverage during the upgrade window.
- [ ] Confirm escalation path is documented.
- [ ] Confirm monitoring dashboards are ready.
- [ ] Confirm alerting is enabled and reviewed.
- [ ] Confirm log aggregation and audit visibility are available.
- [ ] Confirm a communication channel is active for live upgrade coordination.
- [ ] Pause CI or CD pipelines and do not schedule new application deployments during the cluster upgrade.

## 10. Hard Stop Conditions

- [ ] No deprecated APIs remain in active use for the target version.
- [ ] No incompatible add-ons or controllers remain.
- [ ] A tested restore or failover path exists.
- [ ] Sufficient node replacement capacity exists.
- [ ] Worker nodes are within supported version skew and are not newer than the control plane.
- [ ] Required free subnet IP capacity exists, including the minimum extra IPs needed for rolling node replacement.
- [ ] PodDisruptionBudgets will not block required node drains.
- [ ] Rollback or failover plan is realistic and approved.

## Go / No-Go Signoff

- [ ] Technical readiness reviewed.
- [ ] Application readiness reviewed.
- [ ] Business approval received.
- [ ] Final go decision approved.

## Notes

- Date executed: `________________________`
- Executed by: `________________________`
- Outcome: `________________________`
- Follow-up actions: `________________________`
