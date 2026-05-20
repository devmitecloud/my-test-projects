# Mini EKS Upgrade Checklist

## Core Rules
New EKS releases come roughly every 14 weeks (3 months).
- [ ] Upgrade incrementally only, one minor version at a time.
- [ ] If upgrading across multiple versions, document every hop, for example `1.31 -> 1.32 -> 1.33 -> 1.34`.
NOTE: the cluster cannot be downgraded.

## Upgrade Order

- [ ] Upgrade the control plane first.
- [ ] After the control plane upgrade, upgrade add-ons and worker nodes.
Add-ons and worker nodes can be interchanged only after the control plane upgrade is complete.
- [ ] Do not upgrade add-ons or worker nodes before the control plane.

## Version Rules

- [ ] Confirm the control plane version is the same as the worker node version at the start of the upgrade.
- [ ] Confirm worker nodes are never newer than the control plane.
- [ ] Confirm worker nodes are either the same version as the control plane or up to two minor versions lower.
Example: if the control plane is `1.34`, worker nodes can be `1.34`, `1.33`, or `1.32`, but not `1.35`.

## Prerequisites

- [ ] Check the release notes for each version in the upgrade path.
- [ ] Use [`Kubent`](https://github.com/doitintl/kube-no-trouble) or [`Pluto`](https://github.com/FairwindsOps/pluto) tools for this where possible.
- [ ] Review changelogs for deprecated APIs and required manifest updates.
- [ ] Update manifest files where deprecated or changed API versions are used.
Note: the control plane can only be upgraded, not downgraded.
- [ ] Make and validate changes in lower environments first: `dev -> UAT -> prod`.
- [ ] Confirm at least 5 available IPs for rolling worker node upgrades.
- [ ] Confirm add-ons are compatible with the new version.
- [ ] Take backups where required. If configuration is already stored in Git or YAML, document that as the recovery source.
- [ ] Notify all stakeholders.
- [ ] Do not schedule new deployments during the cluster upgrade. 
- [ ] Make nodes unschedulable during node replacement so no new pods are scheduled onto nodes being upgraded.
- [ ] Add new node group ` on new version`
- [ ] Drain and cordon the Nodes yourself.
- [ ] remove old nodes

Summary of steps - 
- [ ] Upgrade versions e.g `1.33 -> 1.34`.
- [ ] Add new node group ` on 1.34`
- [ ] run `kubent` or `pluto` to see if theres anything that needs to be on new version.
- [ ] Drain and cordon the Nodes yourself.
- [ ] run `kubent` or `pluto`  again to see if everything is alright.
- [ ] remove old nodes
