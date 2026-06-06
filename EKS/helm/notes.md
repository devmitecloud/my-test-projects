# This covers learning of Helm. 

- this covers learning/practicing k8s helm implementation. I am using docker desktop so far to spin up single node cluster.
## what is Helm? 
- Helm automates the creation, packaging, configuration, and deployment of Kubernetes applications by combining configuration files into a single reusable package.

## what is Helm Chart
- A Helm chart is a package that contains all the resources you need to deploy an application to a Kubernetes cluster. This package has YAML files for deployments, services, secrets, and config maps that set up your application as needed.

# Helm Install 

## Introduction
- We will use the following commands as part of this demo
- helm repo list
- helm repo add
- helm repo update
- helm search repo
- helm install
- helm list
- helm uninstall

## List, Add and Search Helm Repository
- The bitnami and artifactory.hub are example repositories (repo) that contains packages and helm charts e.g nginx application package.
- [Bitnami Applications packaged using Helm](https://bitnami.com/stacks/helm)
- [Search for Helm Charts at Artifacthub.io](https://artifacthub.io/)
```t
# List Helm Repositories
helm repo list

# Add Helm Repository
helm repo add <DESIRED-NAME> <HELM-REPO-URL>
helm repo add mybitnami https://charts.bitnami.com/bitnami

# List Helm Repositories
helm repo list

# Search Helm Repository
helm search repo <KEY-WORD>
helm search repo nginx
helm search repo apache
helm search repo wildfly
```

## Install Helm Chart
- Installs the Helm Chart
```t
# Update Helm Repo
helm repo update  # Make sure we get the latest list of charts

# Install Helm Chart
helm install <RELEASE-NAME> <repo_name_in_your_local_desktop/chart_name>
helm install mynginx mybitnami/nginx
```

## List Helm Releases
- This command lists all of the releases for a specified namespace
```t
# List Helm Releases (Default Table Output)
helm list 
helm ls

# List Helm Releases (YAML Output)
helm list --output=yaml

# List Helm Releases (JSON Output)
helm list --output=json

# List Helm Releases with namespace flag
helm list --namespace=default
helm list -n default
```

## List Kubernetes Resources
```t
# List Kubernetes Pods
kubectl get pods

# List Kubernetes Services
kubectl get svc
Observation: Review the EXTERNAL-IP field and you will see it as localhost. Access the nginx page from local desktop localhost

# Access Nginx Application on local desktop browser
http://localhost:80
http://127.0.0.1:80

# Access Application using curl command
curl http://localhost:80
curl http://127.0.0.1:80
```
## Uninstall Helm Release - NO FLAGS
```t
# List Helm Releases
helm ls

# Uninstall Helm Release
helm uninstall <RELEASE-NAME>
helm uninstall mynginx 
```
# Helm Upgrade with set option

## Step-01: Introduction
- We are going to upgrade the HELM RELEASE using `helm upgrade` command in combination with `--set "image.tag=<DOCKER-IMAGE-TAGS>`
- We will use the following Helm Commands in this demo.
- helm repo 
- helm search repo
- helm install
- helm upgrade
- helm history
- helm status

## Step-02: Custom Helm Repo
### Step-02-01: Review our Custom Helm Repo
- [StackSimplify Helm Repo hosted on GitHub](https://stacksimplify.github.io/helm-charts/)
- [GitHub Repository for StackSimplify Helm Repo](https://github.com/stacksimplify/helm-charts)
- [artifacthub.io](https://artifacthub.io): Search for `stacksimplify`
- [mychart1 from artifacthub.io](https://artifacthub.io/packages/helm/stacksimplify/mychart1)


### Step-02-02: Add Custom Helm Repo
```t
# List Helm Repositories
helm repo list

# Add Helm Repository
helm repo add <DESIRED-NAME> <HELM-REPO-URL>
helm repo add stacksimplify https://stacksimplify.github.io/helm-charts/

# List Helm Repositories
helm repo list

# Search Helm Repository
helm search repo <KEY-WORD>
helm search repo mychart1
```

## Step-03: Install Helm Chart from our Custom Helm Repository
```t
# Install myapp1 Helm Chart
helm install <RELEASE-NAME> <repo_name_in_your_local_desktop/chart_name>
helm install myapp1 stacksimplify/mychart1 
```
## Step-04: List Resources and Access Application in Browser
```t
# List Helm Release
helm ls 
or 
helm list

# List Pods
kubectl get pods

# List Services 
kubectl get svc

# Access Application
http://localhost:<NODE-PORT>
http://localhost:31231
```

## Step-04: Helm Upgrade
- [kubenginx Docker Image with 1.0.0, 2.0.0, 3.0.0, 4.0.0](https://github.com/users/stacksimplify/packages/container/package/kubenginx)
```t
# Review the Docker Image Versions we are using
https://github.com/users/stacksimplify/packages/container/package/kubenginx
Image Tags: 1.0.0, 2.0.0, 3.0.0, 4.0.0

# Helm Upgrade
helm upgrade <RELEASE-NAME> <repo_name_in_your_local_desktop/chart_name> --set <OVERRIDE-VALUE-FROM-values.yaml>
helm upgrade myapp1 stacksimplify/mychart1 --set "image.tag=2.0.0"
```
## Step-05: List Resources after helm upgrade
```t
# List Helm Releases
helm list 
Observation: We should see Revision as 2

# Additional List commands
helm list --superseded
helm list --deployed

# List and Describe Pod
kubectl get pods
kubectl describe pod <POD-NAME> 
Observation: In the Pod Events you should find that "ghcr.io/stacksimplify/kubenginx:2.0.0" is pulled or if already exists on desktop it will be used to create this new pod

# Access Application
http://localhost:<NODE-PORT>
http://localhost:31231
Observation: Version 2 of application should be displayed
```

## Step-06: Do two more helm upgrades - For practice purpose
```t
# Helm Upgrade to 3.0.0
helm upgrade myapp1 kalyan-repo/myapp1 --set "image.tag=3.0.0"

# Access Application
http://localhost:<NODE-PORT>
http://localhost:31231

# Helm Upgrade to 4.0.0
helm upgrade myapp1 kalyan-repo/myapp1 --set "image.tag=4.0.0"

# Access Application
http://localhost:<NODE-PORT>
http://localhost:31231
```

## Step-07: Helm History
- History prints historical revisions for a given release.
```t
# helm history
helm history RELEASE_NAME
helm history myapp1
```

## Step-08: Helm Status
- This command shows the status of a named release. 
```t
# Helm Status
helm status RELEASE_NAME
helm status myapp1

# Helm Status - Show Description (display the description message of the named release)
helm status myapp1 --show-desc    

# Helm Status - Show Resources (display the resources of the named release)
helm status myapp1  

# Helm Status - revision (display the status of the named release with revision)
helm status RELEASE_NAME --revision int
helm status myapp1 --revision 2
```

## Step-09: Uninstall Helm Release
```t
# Uninstall Helm Release
helm uninstall myapp1
```

# Helm Upgrade with Chart Versions

## Step-01: Introduction
- We are going to learn some additional flags for `helm search repo` command
- We are going to Install and Upgrade Helm Releases using Chart Versions
- In addition, we are going to learn about Helm Rollback 
- helm install
- helm search repo
- helm status
- helm upgrade
- helm rollback
- helm history

## Step-02: Search Helm Repo for mychart2
- [Review mychart2 in Github Repo](https://github.com/stacksimplify/helm-charts/tree/main)
- mychart2 has 4 chart versions (0.1.0, 0.2.0, 0.3.0, 0.4.0)
- mychart2 Chart Versions -> App Version
- 0.1.0 -> 1.0.0
- 0.2.0 -> 2.0.0
- 0.3.0 -> 3.0.0
- 0.4.0 -> 4.0.0
- [Review Artifacthub.io](https://artifacthub.io/packages/helm/stacksimplify/mychart2/)
```t
# Search Helm Repo
helm search repo mychart2
Observation: Should display latest version of mychart2 from stacksimplify helm repo

# Search Helm Repo with --versions
helm search repo mychart2 --versions
Observation: Should display all versions of mychart2

# Search Helm Repo with --version
helm search repo mychart2 --version "CHART-VERSIONS"
helm search repo mychart2 --version "0.2.0"
Observation: Should display specified version of helm chart 
```

## Step-03: Install Helm Chart by specifying Chart Version
```t
# Install Helm Chart by specifying Chart Version
helm install myapp101 stacksimplify/mychart2 --version "CHART-VERSION"
helm install myapp101 stacksimplify/mychart2 --version "0.1.0"

# List Helm Release
helm list 

# List Kubernetes Resources Deployed as part of this Helm Release
helm status myapp101 

# Access Application
http://localhost:31232

# View Pod logs
kubectl get pods
kubectl logs -f POD-NAME
```

## Step-04: Helm Upgrade using Chart Version
```t
# Helm Upgrade using Chart Version
helm upgrade myapp101 stacksimplify/mychart2 --version "0.2.0"

# List Helm Release
helm list 

# List Kubernetes Resources Deployed as part of this Helm Release
helm status myapp101 

# Access Application
http://localhost:31232

# List Release History
helm history myapp101
```

## Step-05: Helm Upgrade without Chart Version
```t
# Helm Upgrade using Chart Version
helm upgrade myapp101 stacksimplify/mychart2

# List Helm Release
helm list 

# List Kubernetes Resources Deployed as part of this Helm Release
helm status myapp101 

# Access Application
http://localhost:31232
Observation: Should take the latest release which is Appversion 4.0.0, Chart Version 0.4.0 (Which is default or latest Chart version)

# List Release History
helm history myapp101
```

## Step-06: Helm Rollback
- Roll back a release to a previous revision or a specific revision
```t
# Rollback to previous version
helm rollback RELEASE-NAME 
helm rollback myapp101

# List Helm Release
helm list 

# List Kubernetes Resources Deployed as part of this Helm Release
helm status myapp101 

# Access Application
http://localhost:31232
Observation: Should see V2 version of Application (Chart Version 0.2.0, AppVersion 2.0.0)

# List Release History
helm history myapp101
```

## Step-07: Helm Rollback to specific Revision
- Roll back a release to a previous revision or a specific revision
```t
# Rollback to previous version
helm rollback RELEASE-NAME REVISION
helm rollback myapp101 1

# List Helm Release
helm list 

# List Kubernetes Resources Deployed as part of this Helm Release
helm status myapp101 

# Access Application
http://localhost:31232
Observation: Should see V1 version of Application (Chart Version 0.1.0, AppVersion 1.0.0)

# List Release History
helm history myapp101
```

# Helm Uninstall Keep History 

## Step-01: Introduction
- We will learn to uninstall Helm Release in a most effective way (best practice) so that we don't loose the history of our Helm Release
- **Important Note:** This demo is in continuation to previous release demo

## Step-02: Uninstall Helm Release with --keep-history Flag
```t
# List Helm Releases
helm list
helm list --superseded
helm list --deployed

# List Release History
helm history myapp101

# Uninstall Helm Release with --keep-history Flag
helm uninstall <RELEASE-NAME> --keep-history
helm uninstall myapp101 --keep-history

# List Helm Releases which are uninstalled
helm list --uninstalled
Observation:
We should see uninstalled release

# helm status command
helm status myapp101
Observation:
1. works only when we use --keep-history flag
2. We can see all the details of release with "Status: Uninstalled"
```

## Step-03: Rollback Uninstalled Release
```t
# List Release History
helm history myapp101

# Rollback Helm Uninstalled Release
helm rollback <RELEASE> [REVISION] [flags]
helm rollback myapp101 3
Observation: It should rollback to specific revision number from revision history

# List Helm Releases
helm list

# List Kubernetes Resources
kubectl get pods
kubectl get svc

# List Kubernetes Resources Deployed as part of this Helm Release
helm status myapp101 

# Access Application 
http://localhost:31232
```

## Step-04: Uninstall Helm Release - NO FLAGS
```t
# List Helm Releases
helm list

# Uninstall Helm Release
helm uninstall <RELEASE-NAME>
helm uninstall myapp101

# List Helm Releases which are uninstalled
helm list --uninstalled
Observation:
We should not see uninstalled release, this command will completely remove the release and its all references

# helm status command
helm status myapp101
Observation:
As the release is permanently removed, we dont get an error "Error: release: not found"

# List Helm History
helm history myapp101
```

## Step-05: Rollback Uninstalled Release
```t
# Rollback Helm Uninstalled Release
helm rollback <RELEASE> [REVISION] [flags]
helm rollback myapp101 1 
Observation: 
Should throw error "Error: release: not found"
```

## Step-06: Best Practice for Helm Uninstall
- It is recommended to always use `--keep-history Flag` for following reasons
- Keeping Track of uninstalled releases
- Quick Rollback if that Release is required

# Helm Install with Generate Name Flag

## Step-01: Introduction
- `--generate-name` flag for `helm install` is very very important option
- This is one of the good to know option from `helm install` perspective
- When we are implementing DevOps Pipelines, if we want to generate the names of our releases without throwing duplicate release errors we can use this setting. 

## Step-02: Install helm with --generate-name flag
```t
# Install helm with --generate-name flag
helm install <repo_name_in_your_local_desktop/chart_name> --generate-name
helm install stacksimplify/mychart1 --generate-name

# List Helm Releases
helm list
helm list --output=yaml
Observation:
We can see the name as "name: mychart1-1689683948" some auto-generated number

# Helm Status
helm status mychart1-1689683948 
helm status mychart1-1689683948 

# Access Application
http://localhost:31231
```
## Step-03: Uninstall Helm Release
```t
# Uninstall Helm Release
helm uninstall <RELEASE-NAME>
helm uninstall mychart1-1689683948
```

# Helm Install Atomic Flag ( replaced now with --rollback-on-failure)

## Step-01: Introduction
- We will learn to use `--rollback-on-failure` flag when installing the Helm Release and also understand the importance of using it in a practical way

## Step-02: Install Helm Chart - Release: dev101
```t
# Install Helm Chart 
helm install dev101 stacksimplify/mychart1

# List Helm Release
helm list 

# List Kubernetes Resources Deployed as part of this Helm Release
helm status dev101 

# Access Application
http://localhost:31231
```

## Step-03: Install Helm Chart - Release: qa101
```t
# Install Helm Chart 
helm install qa101 stacksimplify/mychart1

# List Helm Release
helm list 
Observation: You should see qa101 release installed with FAILED status

Error: INSTALLATION FAILED: 1 error occurred:
	* Service "qa101-mychart1" is invalid: spec.ports[0].nodePort: Invalid value: 31231: provided port is already allocated

# Uninstall qa101 release which is in failed state
helm uninstall qa101

# List Helm Release
helm list 
```


## Step-04: Install Helm Chart - Release: qa101 with --atomic flag
- when `--atomic` flagis set, the installation process deletes the installation on failure. 
- The `--wait` flag will be set automatically if `--atomic` is used
- `--wait` will wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. It will wait for as long as `--timeout`
- `--timeout`  time to wait for any individual Kubernetes operation (like Jobs for hooks) (default 5m0s)
```t
# Install Helm Chart 
helm install qa101 stacksimplify/mychart1 --atomic ( deprecated and replaced with --rollback-on-failure)
correct way
helm install qa101 stacksimplify/mychart1 --rollback-on-failure 


# List Helm Release
helm list 
Observation: We will not see qa101 FAILED release, --atomic flag deleted the release as soon as it is failed with error

Error: INSTALLATION FAILED: 1 error occurred:
	* Service "qa101-mychart1" is invalid: spec.ports[0].nodePort: Invalid value: 31231: provided port is already allocated
```

## Step-05: Uninstall dev101 Release
```t
# Uninstall dev101 release
helm uninstall dev101

# List Helm Releases
helm list
```

# Helm with Kubernetes Namespaces

## Step-01: Introduction
- Any resource we manage using HELM are specific to Kubernetes Namespace
- By default, Kubernetes resources deployed to k8s cluster using default namespace, so we don't need to specify namespace name explicitly
- In the case if we want to deploy k8s resources to a namespace (other than default), then we need to specify that in `helm install` command with flag `--namespace` or `-n`
- In addition, we can also create a namespace during `helm install` using flags `--namespace`  `--create-namespace` 

## Step-02: Install Helm Release by creating Kubernetes Namespace dev
```t
# List Kubernetes Namespaces 
kubectl get ns

# Install Helm Release by creating Kubernetes Namespace
helm install dev101 stacksimplify/mychart2 --version "0.1.0" --namespace dev --create-namespace 

# List Kubernetes Namespaces 
kubectl get ns
Observation: Found the dev namespace created as part of `helm install`

# List Helm Release
helm list --> NO RELEASES in default namespace
helm list -n dev
helm list --namespace dev

# Helm Status
helm status dev101  -n dev
helm status dev101  --namespace dev

# List Kubernetes Pods
kubectl get pods -n dev
kubectl get pods --namespace dev

# List Services
kubectl get svc -n dev

# List Deployments
kubectl get deploy -n dev

# Access Application
http://localhost:31232
```

## Step-03: Run helm upgrade for resources present in dev namespace
```t
# Helm Upgrade
helm upgrade dev101 stacksimplify/mychart2 --version "0.2.0" --namespace dev 
or
helm upgrade dev101 stacksimplify/mychart2 --version "0.2.0" -n dev

# List Helm Release
helm list -n dev
helm list --namespace dev

# Helm Status
helm status dev101  -n dev
helm status dev101  --namespace dev

# Access Application
http://localhost:31232
```

## Step-04: Uninstall Helm Release from dev Namespace
```t
# Uninstall Helm Releas
helm uninstall dev101 --namespace dev
helm uninstall dev101 -n dev

# List Helm Release
helm list -n dev
helm list --namespace dev

# List Kubernetes Namespaces
kubectl get ns
Observation: 
1. When uninstalling helm release, it will not delete the Kubernetes Resource: dev namespace. 
2. If we dont need that dev namespace we need to manually delete it from kubernetes using kubectl
3. we can get the k8s manifest for all resources in deployed in the namesapace for the app release by helm using 
   ``` helm get manifest dev101 -n dev ```
# Delete dev namespace
kubectl delete ns dev

# List Kubernetes Namespaces
kubectl get ns
```

# Helm Override default values from values.yaml

## Step-01: Introduction
- We will learn the following in this section
    - helm install --set 
    - helm upgrade -f myvalues.yaml
    - **--dry-run=client:**
    - **--debug:** 
    - helm get values
    - helm get values --revision
    - helm get manifest
    - helm get manifest --revision
    - helm get all
- Discuss about Values Hierarchy

## Step-02: Override default NodePort 31231 with --set
### Step-02-01: Review our mychart1 Helm Chart values.yaml
- [mychart1 values.yaml](https://github.com/stacksimplify/helm-charts/blob/main/mychart1/values.yaml)

### Step-02-02: Learn about --dry-run=client and --debug flags for helm install command
- Install Helm Chart by overriding NodePort 31231 with 31240
```t
# Helm Install with --dry-run=client command
helm install myapp901 stacksimplify/mychart1 --set service.nodePort=31240 --dry-run=client 

# Helm Install with --dry-run=client and --debug command
helm install myapp901 stacksimplify/mychart1 --set service.nodePort=31240 --dry-run=client --debug

## THE BELOW IS THE SAMPLE OUTPUT WITH DEBUG ADDED
NAME: myapp901
NAMESPACE: default
STATUS: pending-install
REVISION: 1
	USER-SUPPLIED VALUES:
service:
  nodePort: 31240
COMPUTED VALUES:
fullnameOverride: ""
image:
  pullPolicy: IfNotPresent
  repository: ghcr.io/stacksimplify/kubenginx
  tag: ""
nameOverride: ""
podAnnotations: {}
replicaCount: 1
service:
  nodePort: 31240
  port: 80
  type: NodePort
```

### Step-02-03: helm install with --set and test
```t
# Helm Install 
helm install myapp901 stacksimplify/mychart1 --set service.nodePort=31240 

# helm status 
helm status myapp901 
Observation:
We can see that our NodePort service is running on port 31240

# Access Application
http://localhost:31240
```

## Step-03: Review myvalues.yaml
- **myvalues.yaml file location:** 09-Helm-Override-Values/myvalues.yaml
```yaml
# Change-1: change replicas from 1 to 2
replicaCount: 2

# Change-2: Add tag as "2.0.0" which will override the default appversion "1.0.0" from our mychart1
image:
  repository: ghcr.io/stacksimplify/kubenginx
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "2.0.0"

# Change-3: Change nodePort from 31240 to 31250
service:
  type: NodePort
  port: 80
  nodePort: 31250
```

## Step-04: Override NodePort 31240 with -f myvalues.yaml with 
- We can either `-f  myvalues.yaml` or `--values myvalues.yaml`.  Both are valid inputs
```t
# Verify if myvalues.yaml
cd 09-Helm-Override-Values
cat myvalues.yaml

# helm upgrade with --dry-run=client and --debug commands
helm upgrade myapp901 stacksimplify/mychart1 -f myvalues.yaml --dry-run=client --debug

# helm upgrade
helm upgrade myapp901 stacksimplify/mychart1 -f myvalues.yaml

# helm status
helm status myapp901 
Observation: 
1. Two pods will be running as we changed replicacount to 2
2. Service Node Port will be 31250 

# Access Application
http://localhost:31250
Observation: 
1. We should see V2 application because we have used the "image tag as 2.0.0"
```

## Step-05: helm get values command
- **helm get values:** This command downloads a values file for a given release
```t
# helm get values
helm get values RELEASE_NAME
helm get values myapp901
Observation:
1. Provides the values from current/latest release version 2 from Release myapp901

## Sample Output
Kalyans-MacBook-Pro:09-Helm-Override-Values kalyan$ helm get values myapp901
USER-SUPPLIED VALUES:
image:
  pullPolicy: IfNotPresent
  repository: ghcr.io/stacksimplify/kubenginx
  tag: 2.0.0
replicaCount: 2
service:
  nodePort: 31250
  port: 80
  type: NodePort


# helm history (History prints historical revisions for a given release.)
helm history myapp901


# helm get values with --revision
helm get values RELEASE-NAME --revision int
helm get values myapp901 --revision 1

## Sample Output
Kalyans-MacBook-Pro:09-Helm-Override-Values kalyan$ helm get values myapp901 --revision 1
USER-SUPPLIED VALUES:
service:
  nodePort: 31240
```

## Step-06: helm get manifest command 
- **helm get manifest:** This command fetches the generated manifest for a given release.
```t
# helm get manifest
helm get manifest RELEASE-NAME
helm get manifest myapp901

# helm get manifest --revision
helm get manifest RELEASE-NAME --revision int
helm get manifest myapp901 --revision 1
```

## Step-07: helm get all command
- **helm get all:** This command prints a human readable collection of information about the notes, hooks, supplied values, and generated manifest file of the given release.
- This is a good way to see what templates are installed on the kubernetes cluster server.
- **helm get notes and helm get hooks:** These two commmands we will explore when we are discussing about helm chart development. 
```t
# helm get all
helm get all RELEASE-NAME
helm get all myapp901
```

## Step-08: Uninstall Helm Release
```t
# Uninstall Helm Release
helm uninstall myapp901

# List Helm Releases
helm list
```

## Step-09: Values Hierarchy
1. Sub chart `values.yaml` can be overriden by parents chart `values.yaml`
2. Parent charts `values.yaml` can be overriden by user-supplied value file `(-f myvalues.yaml)`
3. User-supplied value file `(-f myvalues.yaml)` can be overriden by `--set` parameters

## Step-10: Deleting a default Key by passing null
- If you need to delete a key from the default values, you may override the value of the key to be null, in which case Helm will remove the key from the overridden values merge.
```t
# Release: myapp901
helm install myapp901 stacksimplify/mychart1 --atomic
helm list
helm status myapp901 
http://localhost:31231

# Release: myapp902
helm install myapp902 stacksimplify/mychart1 --atomic
helm list

# Option-1: Give desired port other than 31231
helm install myapp902 stacksimplify/mychart1 --set service.nodePort=31232 

# Option-2: Pass null value to nodePort (service.nodePort=null)
helm install myapp902 stacksimplify/mychart1 --set service.nodePort=null --dry-run=client --debug
helm install myapp902 stacksimplify/mychart1 --set service.nodePort=null 

# Additional Notes for understanding
1. We will choose option-2 to demonstrate the concept "Deleting a default Key by passing null"
2. For NodePort Service, if we dont define the "nodePort" argument, it by default assigns a port dynamically from the port range 30000-32767. 
3. In our case already 31231 is used, other than that port it will allocate someother port when we pass null. 
4. In short, if we dont want to pass the default values present in values.yaml as-is, we dont need to change the complete chart with a new version, we can just pass null.

# Uninstall Releases
helm uninstall myapp901
helm uninstall myapp902
helm list
```