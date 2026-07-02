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

# Helm Install rollback-on-failure Flag ( replaced now with --rollback-on-failure)

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


## Step-04: Install Helm Chart - Release: qa101 with --rollback-on-failure flag
- when `--rollback-on-failure` flagis set, the installation process deletes the installation on failure. 
- The `--wait` flag will be set automatically if `--rollback-on-failure` is used
- `--wait` will wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. It will wait for as long as `--timeout`
- `--timeout`  time to wait for any individual Kubernetes operation (like Jobs for hooks) (default 5m0s)
```t
# Install Helm Chart 

correct way
helm install qa101 stacksimplify/mychart1 --rollback-on-failure 


# List Helm Release
helm list 
Observation: We will not see qa101 FAILED release, --rollback-on-failure flag deleted the release as soon as it is failed with error

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
helm install myapp901 stacksimplify/mychart1 --rollback-on-failure
helm list
helm status myapp901 
http://localhost:31231

# Release: myapp902
helm install myapp902 stacksimplify/mychart1 --rollback-on-failure
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


# Helm Builtin Objects

## Step-01: Introduction
- Objects are passed into a template from the template engine. 
- Objects can be simple, and have just one value or they can contain other objects or functions. 
- For example: the Release object contains several objects (like .Release.Name) and the Files object has a few functions.
### Helm Builtin Objects
- Release
- Chart 
- Values 
- Capabilities 
- Template 
- Files 

## Step-02: Create a simple chart and clean-up NOTES.txt
```t
# Create Helm Chart
helm create CHART-NAME
helm create builtinobjects

# Remove all content from NOTES.txt
cd builtinobjects/templates
>NOTES.txt

# Change to Chart Directory
cd builtinobjects

# helm install --dry-run
helm install myapp1 . --dry-run
```

## Step-03: Helm Object: Root or dot or Period (.)
```t
# Update NOTES.txt
{{/* Root or Dot or Period Object */}}
Root Object: {{ . }}

# Change to Chart Directory
cd builtinobjects

# helm install with --dry-run
helm install myapp101 . --dry-run
```

## Step-04: Helm Object: Release
- This object describes the Helm release. 
- It has several objects inside it related to Helm Release.
- Put the below in `NOTES.txt` and test it
```t
{{/* Release Object */}}
Release Name: {{ .Release.Name }}
Release Namespace: {{ .Release.Namespace }}
Release IsUpgrade: {{ .Release.IsUpgrade }}
Release IsInstall: {{ .Release.IsInstall }}
Release Revision: {{ .Release.Revision }}
Release Service: {{ .Release.Service }}

# Change to CHART Directory 
cd builtinobjects 

# Helm Install with --dry-run
helm install myapp101 . --dry-run

# Sample Output
NOTES:
Release Name: myapp101
Release Namespace: default
Release IsUpgrade: false
Release IsInstall: true
Release Revision: 1
Release Service: Helm
```

## Step-05: Helm Object: Chart
- Any data in Chart.yaml will be accessible using Chart Object. 
- For example {{ .Chart.Name }}-{{ .Chart.Version }} will print out the builtinobjects-0.1.0.
- [Complte Chart.yaml Objects for reference](https://helm.sh/docs/topics/charts/#the-chartyaml-file)
- Put the below in `NOTES.txt` and test it
```t
{{/* Chart Objet */}}
Chart Name: {{ .Chart.Name }}
Chart Version: {{ .Chart.Version }}
Chart AppVersion: {{ .Chart.AppVersion }}
Chart Type: {{ .Chart.Type }}
Chart Name and Version: {{ .Chart.Name }}-{{ .Chart.Version }}

# Change to CHART Directory 
cd builtinobjects 

# Helm Install with --dry-run
helm install myapp101 . --dry-run

# Sample Output
Chart Name: builtinobjects
Chart Version: 0.1.0
Chart AppVersion: 0.1.0
Chart Type: application
Chart Name and Version: builtinobjects-0.1.0
```

## Step-06: Helm Objects: Values, Capabilities, Template
- **Values Object:** Values passed into the template from the values.yaml file and from user-supplied files. By default, Values is empty.
- **Capabilities Object:** This provides information about what capabilities the Kubernetes cluster supports
- **Template Object:** Contains information about the current template that is being executed
- Put the below in `NOTES.txt` and test it
```t
{{/* Values Object */}}
Replica Count: {{ .Values.replicaCount }}
Image Repository: {{ .Values.image.repository }}
Service Type: {{ .Values.service.type }}

{{/* Capabilities Object */}}
Kubernetes Cluster Version Major: {{ .Capabilities.KubeVersion.Major }}
Kubernetes Cluster Version Minor: {{ .Capabilities.KubeVersion.Minor }}
Kubernetes Cluster Version: {{ .Capabilities.KubeVersion }} and {{ .Capabilities.KubeVersion.Version }}
Helm Version: {{ .Capabilities.HelmVersion }}
Helm Version Semver: {{ .Capabilities.HelmVersion.Version }}

{{/* Template Object */}}
Template Name: {{ .Template.Name }} 
Template Base Path: {{ .Template.BasePath }}

# Change to CHART Directory 
cd builtinobjects 

# Helm Install with --dry-run
helm install myapp101 . --dry-run

# Sample Output
Replica Count: 1
Image Repository: ghcr.io/stacksimplify/kubenginxhelm
Service Type: NodePort

Kubernetes Cluster Version Major: 1
Kubernetes Cluster Version Minor: 27
Kubernetes Cluster Version: v1.27.2 and v1.27.2
Helm Version: {v3.12.1 f32a527a060157990e2aa86bf45010dfb3cc8b8d clean go1.20.5}
Helm Version Semver: v3.12.1

Template Name: builtinobjects/templates/NOTES.txt 
Template Base Path: builtinobjects/templates
```

## Step-07: Helm Objects: Files
- **Files Object:** 
- Put the below in `NOTES.txt` and test it
- [Additional Reference: Access Files Inside Templates](https://helm.sh/docs/chart_template_guide/accessing_files/)
```t
{{/* File Object */}}
File Get: {{ .Files.Get "myconfig1.toml" }}
File Glob as Config: {{ (.Files.Glob "config-files/*").AsConfig }}
File Glob as Secret: {{ (.Files.Glob "config-files/*").AsSecrets }}
File Lines: {{ .Files.Lines "myconfig1.toml" }}
File Lines: {{ .Files.Lines "config-files/myconfig2.toml" }}
File Glob: {{ .Files.Glob "config-files/*" }}

# Change to CHART Directory 
cd builtinobjects 

# Helm Install with --dry-run
helm install myapp101 . --dry-run

# Sample Output
File Get: message1 = Hello from config 1 line1
message2 = Hello from config 1 line2
message3 = Hello from config 1 line3

File Glob as Config: myconfig2.toml: |-
  appName: myapp2
  appType: db
  appConfigEnable: true
myconfig3.toml: |-
  appName: myapp3
  appType: app
  appConfigEnable: false
File Glob as Secret: myconfig2.toml: YXBwTmFtZTogbXlhcHAyCmFwcFR5cGU6IGRiCmFwcENvbmZpZ0VuYWJsZTogdHJ1ZQ==
myconfig3.toml: YXBwTmFtZTogbXlhcHAzCmFwcFR5cGU6IGFwcAphcHBDb25maWdFbmFibGU6IGZhbHNl
File Lines: [message1 = Hello from config 1 line1 message2 = Hello from config 1 line2 message3 = Hello from config 1 line3 ]
File Lines: [appName: myapp2 appType: db appConfigEnable: true]
File Glob: map[config-files/myconfig2.toml:[97 112 112 78 97 109 101 58 32 109 121 97 112 112 50 10 97 112 112 84 121 112 101 58 32 100 98 10 97 112 112 67 111 110 102 105 103 69 110 97 98 108 101 58 32 116 114 117 101] config-files/myconfig3.toml:[97 112 112 78 97 109 101 58 32 109 121 97 112 112 51 10 97 112 112 84 121 112 101 58 32 97 112 112 10 97 112 112 67 111 110 102 105 103 69 110 97 98 108 101 58 32 102 97 108 115 101]]
```

## Additional Reference
- [Helm Built-In Objects](https://helm.sh/docs/chart_template_guide/builtin_objects/)
- [Helm Chart.yaml Fields](https://helm.sh/docs/chart_template_guide/builtin_objects/)


Note: If we use dot(.) inside range and with actions it is going to be current context in that respective block abd bit the Root Helm Object. 
If ppassed in any other lace it will call the Top level Helm Object.
# Helm Template Functions and Pipelines

## Step-01: Introduction
1. Template Actions `{{ }}`
2. Action Elements `{{ .Release.Name }}`
3. Quote Function
4. Pipeline 
5. default Function
6. lower function
7. Controlling White Spaces `{{-  -}}`
7. indent function
8. nindent function
9. toYaml

## Step-02: Template Action "{{ }}"
- Anything in between Template Action `{{ .Chart.Name }}` is called Action Element
- Anything in between Template Action `{{ .Chart.Name }}` will be rendered by helm template engine and replace necessary values
- Anything outside of the template action will be printed as it is.
- Action elements defined inside the `{{ }}` will help us to retrieve data from other sources (example: `.Chart.Name`).
### Step-02-01: Valid Action Element
```t
# deployment.yaml file
apiVersion: apps/v1
kind: Deployment
metadata:
  # Template Action with Action Elements
  name: {{ .Release.Name }}-{{ .Chart.Name }}

# Change to CHART Directory
cd helmbasics

# Helm Template Command
helm template myapp101 .
1. helm template command helps us to check the output of the chart in fully rendered Kubernetes resource templates. 
2. This will be very helpful when we are developing a new chart, making changes to the chart templates, for debugging etc.
```
### Step-02-02: Invalid Action Element 
```t
# deployment.yaml file
apiVersion: apps/v1
kind: Deployment
metadata:
  # Template Action with Action Elements
  name: {{ something }}-{{ .Chart.Name }}
# Change to CHART Directory
cd helmbasics

# Helm Template Command
helm template myapp101 .  
Observation:
1. Should fail with error
2. In short, inside Action Element we should have 

Error: parse error at (helmbasics/templates/deployment.yaml:10): function "something" not defined
```

## Step-03: Template Function: quote
```t
# Add Quote Function 
  annotations:    
    app.kubernetes.io/managed-by: {{ .Release.Service }}
    # quote function
    app.kubernetes.io/managed-by: {{ quote .Release.Service }} 

# Change to CHART Directory
cd helmbasics

# Helm Template Command
helm template myapp101 .
```

## Step-04: Pipeline
- Pipelines are an efficient way of getting several things done in sequence. 
- Inverting the order is a common practice in templates (.val | quote ) 
```t
# Add Quote Function with Pipeline
  annotations:    
    app.kubernetes.io/managed-by: {{ .Release.Service }}
    # quote function
    app.kubernetes.io/managed-by: {{ quote .Release.Service }} 
    # quote function with pipeline
    app.kubernetes.io/managed-by: {{ .Release.Service | quote }}               

# Change to CHART Directory
cd helmbasics

# Helm Template Command
helm template myapp101 .
```

## Step-05: Template Function: default and lower
- [default function](https://helm.sh/docs/chart_template_guide/function_list/#default)
```t
# values.yaml
releaseName: "newrelease101"
replicaCount: 3

# Template Function default
  annotations:
    app.kubernetes.io/managed-by: {{ .Release.Service }}
    # Quote Function
    app.kubernetes.io/managed-by: {{ quote .Release.Service }}        
    # Pipeline
    app.kubernetes.io/managed-by: {{ .Release.Service | quote | upper | lower }}        
    # default Function
    app.kubernetes.io/name: {{ default "MYRELEASE101" .Values.releaseName | lower }}
spec:
  replicas: {{ default 1  .Values.replicaCount }}

# Change to CHART Directory
cd helmbasics

# Helm Template Command
helm template myapp101 .
```

## Step-06: Controlling Whitespaces
- **{{- .Chart.name }}:**  If a hyphen is added before the statement, `{{- .Chart.name }}` then the leading whitespace will be ignored during the rendering
- **{{ .Chart.name -}}:** If a hyphen is added after the statement, `{{ .Chart.name -}}` then the trailing whitespace will be ignored during the rendering
```yaml
  annotations:
    app.kubernetes.io/managed-by: {{ .Release.Service }}
    # Quote Function
    app.kubernetes.io/managed-by: {{ quote .Release.Service }}        
    # Pipeline
    app.kubernetes.io/managed-by: {{ .Release.Service | quote | upper | lower }}        
    # default Function
    app.kubernetes.io/name: {{ default "MYRELEASE101" .Values.releaseName }}
    # Controlling Leading and Trailing White spaces 
    leading-whitespace: "   {{- .Chart.Name }}    kalyan"
    trailing-whitespace: "   {{ .Chart.Name -}}    kalyan"
    leadtrail-whitespace: "   {{- .Chart.Name -}}    kalyan"    

# Change to CHART Directory
cd helmbasics

# Helm Template Command
helm template myapp101 .    
```


## Step-07: indent and nindent functions
- **indent:** The [indent function](https://helm.sh/docs/chart_template_guide/function_list/#indent) indents every line in a given string to the specified indent width. This is useful when aligning multi-line strings:
- **nindent:** The [nindent function](https://helm.sh/docs/chart_template_guide/function_list/#nindent) is the same as the indent function, but prepends a new line to the beginning of the string.

```yaml
# indent and nindent functions
  annotations:
    app.kubernetes.io/managed-by: {{ .Release.Service }}
    # Quote Function
    app.kubernetes.io/managed-by: {{ quote .Release.Service }}        
    # Pipeline
    app.kubernetes.io/managed-by: {{ .Release.Service | quote | upper | lower }}        
    # default Function
    app.kubernetes.io/name: {{ default "MYRELEASE101" .Values.releaseName | lower }}
    # Controlling Leading and Trailing White spaces 
    leading-whitespace: "   {{- .Chart.Name }}    kalyan"
    trailing-whitespace: "   {{ .Chart.Name -}}    kalyan"
    leadtrail-whitespace: "   {{- .Chart.Name -}}    kalyan"  
    # indent function
    indenttest: "  {{- .Chart.Name | indent 4 -}}  "
    # nindent function
    nindenttest: "  {{- .Chart.Name | nindent 4 -}}  "  

# Change to CHART Directory
cd helmbasics

# Helm Template Command
helm template myapp101 .    
```

## Step-08: Template Function: toYaml 
- **toYaml:** 
- We can use [toYaml function](https://helm.sh/docs/chart_template_guide/function_list/#type-conversion-functions) inside the helm template actions to convert an object into YAML.
- Convert list, slice, array, dict, or object to indented yaml. 
```t
# values.yaml
# Resources for testing Template Function: toYaml 
resources: 
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi

# deployment.yaml
    spec:
      containers:
      - name: nginx
        image: ghcr.io/stacksimplify/kubenginx:4.0.0
        ports:
        - containerPort: 80
        resources: 
        {{- toYaml .Values.resources | nindent 10}}

# Change to CHART Directory
cd helmbasics

# Helm Template Command
helm template myapp101 .

# Helm Install with --dry-run
helm install myapp101 . --dry-run

# Helm Install
helm install myapp101 . --rollback-on-failure

# List k8s Pods
kubectl get pods 

# Describe Pod
kubectl describe pod <POD-NAME>

# Helm Uninstall
helm uninstall myapp101
```




# Helm Development - Flow Control If-Else

## Step-01: Introduction
-  We can use `if/else` for creating conditional blocks in Helm Templates
- **eq:** For templates, the operators (eq, ne, lt, gt, and, or and so on) are all implemented as functions. 
- In pipelines, operations can be grouped with parentheses ((, and )).
- [Additional Reference: Operators are functions](https://helm.sh/docs/chart_template_guide/functions_and_pipelines/#operators-are-functions)
### IF-ELSE Syntax
```t
{{ if PIPELINE }}
  # Do something
{{ else if OTHER PIPELINE }}
  # Do something else
{{ else }}
  # Default case
{{ end }}
```

## Step-02: Review values.yaml
```yaml
# If, else if, else
myapp:
  env: prod
```


## Step-03: Logic and Flow Control Function: and 
- [Logic and Flow Control Functions](https://helm.sh/docs/chart_template_guide/function_list/#logic-and-flow-control-functions)
- **eq:**  Returns the boolean equality of the arguments (e.g., Arg1 == Arg2).
```t
# and Syntax
eq .Arg1 .Arg2
```

## Step-04: Implement if-else for replicas
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
  labels:
    app: nginx
spec:
{{- if eq .Values.myapp.env "prod" }}
  replicas: 4 
{{- else if eq .Values.myapp.env "qa" }}  
  replicas: 2
{{- else }}  
  replicas: 1
{{- end }}  
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: ghcr.io/stacksimplify/kubenginx:4.0.0
        ports:
        - containerPort: 80
```

## Step-05: Verify if-else
```t
# Change to Chart Directory
cd helmbasics

# Helm Template (when env: prod from values.yaml)
## TEST IF STATEMENT
helm template myapp1 .

# Helm Template (when env: qa using --set)
## TEST ELSE IF STATEMENT
helm template myapp1 . --set myapp.env=qa
 
# Helm Template (when env: dev or env: null using --set)
## TEST ELSE STATEMENT
helm template myapp1 . --set myapp.env=dev

# Helm Install Dry-run 
helm install myapp1 . --dry-run

# Helm Install
helm install myapp1 . --rollback-on-failure

# Verify Pods
helm status myapp1 --show-resources

# Uninstall Release
helm uninstall myapp1
```

# Helm Development - Flow Control If-Else with Boolean Check and "AND Function"

## Step-01: Introduction
-  We can use `if/else` for creating conditional blocks in Helm Templates
- **eq:** For templates, the operators (eq, ne, lt, gt, and, or and so on) are all implemented as functions. 
- In pipelines, operations can be grouped with parentheses ((, and )).
- [Additional Reference: Operators are functions](https://helm.sh/docs/chart_template_guide/functions_and_pipelines/#operators-are-functions)
### IF-ELSE Syntax
```t
{{ if PIPELINE }}
  # Do something
{{ else if OTHER PIPELINE }}
  # Do something else
{{ else }}
  # Default case
{{ end }}
```

## Step-02: Review values.yaml
```yaml
# If, else if, else
myapp:
  env: prod
  retail:
    enableFeature: true
```

## Step-03: Logic and Flow Control Function: and 
- [Logic and Flow Control Functions](https://helm.sh/docs/chart_template_guide/function_list/#logic-and-flow-control-functions)
- **and:**  Returns the boolean AND of two or more arguments (the first empty argument, or the last argument).
```t
# and Syntax
and .Arg1 .Arg2
```
## Step-04: Implement if-else for replicas with Boolean 

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
  labels:
    app: nginx
spec:
{{- if and .Values.myapp.retail.enableFeature (eq .Values.myapp.env "prod") }}
  replicas: 6
{{- else if eq .Values.myapp.env "prod" }}
  replicas: 4
{{- else if eq .Values.myapp.env "qa" }}  
  replicas: 2
{{- else }}  
  replicas: 1  
{{- end }}
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: ghcr.io/stacksimplify/kubenginx:4.0.0
        ports:
        - containerPort: 80
```

## Step-05: Verify if-else
```t
# Change to Chart Directory
cd helmbasics

# Helm Template 
helm template myapp1 . --set myapp.retail.enableFeature=true
helm template myapp1 . --set myapp.retail.enableFeature=false
helm template myapp1 . --set myapp.env=qa
helm template myapp1 . --set myapp.env=dev

# Helm Install Dry-run 
helm install myapp1 . --set myapp.retail.enableFeature=true --dry-run

# Helm Install
helm install myapp1 . --set myapp.retail.enableFeature=true --rollback-on-failure

# Verify Pods
helm status myapp1 --show-resources

# Uninstall Release
helm uninstall myapp1
```


# Helm Development - Flow Control If-Else with OR Function

## Step-01: Introduction
-  We can use `if/else` for creating conditional blocks in Helm Templates
- **eq:** For templates, the operators (eq, ne, lt, gt, and, or and so on) are all implemented as functions. 
- In pipelines, operations can be grouped with parentheses ((, and )).
- [Additional Reference: Operators are functions](https://helm.sh/docs/chart_template_guide/functions_and_pipelines/#operators-are-functions)
### IF-ELSE Syntax
```t
{{ if PIPELINE }}
  # Do something
{{ else if OTHER PIPELINE }}
  # Do something else
{{ else }}
  # Default case
{{ end }}
```

## Step-02: Review values.yaml
```yaml
# If, else if, else
myapp:
  env: prod
```

## Step-03: Logic and Flow Control Function: and 
- [Logic and Flow Control Functions](https://helm.sh/docs/chart_template_guide/function_list/#logic-and-flow-control-functions)
- **or:**  Returns the boolean OR of two or more arguments (the first non-empty argument, or the last argument).
```t
# and Syntax
or .Arg1 .Arg2

```
## Step-04: Implement if-else for replicas with OR 

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
  labels:
    app: nginx
spec:
{{- if or (eq .Values.myapp.env "prod") (eq .Values.myapp.env "uat") }}
  replicas: 6
{{- else if eq .Values.myapp.env "qa" }}  
  replicas: 2
{{- else }}  
  replicas: 1  
{{- end }}
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: ghcr.io/stacksimplify/kubenginx:4.0.0
        ports:
        - containerPort: 80
```

## Step-05: Verify if-else
```t
# Change to Chart Directory
cd helmbasics

# Helm Template 
helm template myapp1 . --set myapp.env=prod
helm template myapp1 . --set myapp.env=uat
helm template myapp1 . --set myapp.env=dev
helm template myapp1 . --set myapp.env=null


# Helm Install Dry-run 
helm install myapp1 . --dry-run

# Helm Install
helm install myapp1 . --rollback-on-failure

# Verify Pods
helm status myapp1 --show-resources

# Uninstall Release
helm uninstall myapp1
```


# Helm Development - Flow Control If-Else

## Step-01: Introduction
-  We can use `if/else` for creating conditional blocks in Helm Templates
- **eq:** For templates, the operators (eq, ne, lt, gt, and, or and so on) are all implemented as functions. 
- In pipelines, operations can be grouped with parentheses ((, and )).
- [Additional Reference: Operators are functions](https://helm.sh/docs/chart_template_guide/functions_and_pipelines/#operators-are-functions)
### IF-ELSE Syntax
```t
{{ if PIPELINE }}
  # Do something
{{ else if OTHER PIPELINE }}
  # Do something else
{{ else }}
  # Default case
{{ end }}
```

## Step-02: Review values.yaml
```yaml
# If, else if, else
myapp:
  env: prod
```

## Step-03: Logic and Flow Control Function: and 
- [Logic and Flow Control Functions](https://helm.sh/docs/chart_template_guide/function_list/#logic-and-flow-control-functions)
- **not:**  Returns the boolean negation of its argument.
```t
# and Syntax
not .Arg
```
## Step-04: Implement if-else for replicas with OR 

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
  labels:
    app: nginx
spec:
{{- if not (eq .Values.myapp.env "prod") }}
  replicas: 1
{{- else }}  
  replicas: 6
{{- end }}
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: ghcr.io/stacksimplify/kubenginx:4.0.0
        ports:
        - containerPort: 80
```

## Step-05: Verify if-else
```t
# Change to Chart Directory
cd helmbasics

# Helm Template
helm template myapp1 . --set myapp.env=prod
helm template myapp1 . --set myapp.env=dev
helm template myapp1 . --set myapp.env=null

# Helm Install Dry-run 
helm install myapp1 . --dry-run

# Helm Install
helm install myapp1 . --rollback-on-failure

# Verify Pods
helm status myapp1 --show-resources

# Uninstall Release
helm uninstall myapp1
```


# Helm Development - Flow Control With 

## Step-01: Introduction
- `with` action controls variable scoping. 
- `with` action can allow you to set the current scope (.) to a particular object. 
### with action Syntax
```t
{{ with PIPELINE }}
  # restricted scope
{{ end }}
```
## Step-02: Review values.yaml
```yaml
# For testing Flow Control: with 
podAnnotations: 
  appName: myapp1
  appType: webserver
  appTech: HTML
```

## Step-03: Implement "with" action
- `with` action statement sets the dot obejct "." to `.Values.podAnnotations` 
- Inside the `with` action block dot "." always refers to `.Values.podAnnotations` 
- Outside the `with` action block dot "." refers to Root Object
```yaml
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}        
      {{- end }}    
```

## Step-04: Test the "with" action Implementation
```t
# Change to Chart Directory
cd helmbasics  

# Helm Template
helm template myapp101 .

# Helm Install with dry-run
helm install myapp101 . --dry-run  

# Observation:
We should see all the annotations displayed
      annotations:
        appName: myapp1
        appTech: HTML
        appType: webserver
```

## Step-05: Try to access any Root Object in "with" action block
```t
# Add Root Object in with Block
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
        appManagedBy: {{ .Release.Service }}
      {{- end }}    

# Change to Chart Directory
cd helmbasics  

# Helm Template
helm template myapp101 .

# Helm Install with dry-run
helm install myapp101 . --dry-run  

# Observation:
1. It should throw an error and fail because .Release.Service is not inside of the restricted scope for . which refers to ".Values.podAnnotations". 

## Sample Error
Error: template: helmbasics/templates/deployment.yaml:23:33: executing "helmbasics/templates/deployment.yaml" at <.Release.Service>: nil pointer evaluating interface {}.Service
```

## Step-06: Add $ to Root Object
- To access Root Objects inside `with` action block we need to prepend that Root object with `$`
```t
# To Access Root Object
       appManagedBy: {{ $.Release.Service }}

 # Change to Chart Directory
cd helmbasics  

# Helm Template
helm template myapp101 .

# Helm Install with dry-run
helm install myapp101 . --dry-run  

# Observation:
1. It should work as expected
      annotations:
        appName: myapp1
        appTech: HTML
        appType: webserver
        appManagedBy: Helm  
```

## Step-07: Scope more detailed for "with" action block
- How to retrieve a single object from `.Values.myapps.data.config` ?
- What if there is only need for 1 or 2 values from `.Values.myapps.data.config` ?
- How to access each key value from `.Values.myapps.data.config` ?
```yaml
# values.yaml
# For testing Flow Control: with - Scope more detailed
myapps:
  data: 
    config: 
      appName: myapp1
      appType: webserver
      appTech: HTML
      appDb: mysql

# Current Scope: Retrieve single object using scope
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
data: 
{{- with .Values.myapps.data.config }}
  application-name: {{ .appName }}
  application-type: {{ .appType }}
{{- end}} 

 # Change to Chart Directory
cd helmbasics  

# Helm Template
helm template myapp101 .

# Helm Install with dry-run
helm install myapp101 . --dry-run  

# Observation:
1. We should be able to get values for {{ .appName }} and {{ .appType }}
```


# Helm Development - Flow Control If-Else

## Step-01: Introduction
-  We can use `if/else` for creating conditional blocks in Helm Templates
- **eq:** For templates, the operators (eq, ne, lt, gt, and, or and so on) are all implemented as functions. 
- In pipelines, operations can be grouped with parentheses ((, and )).
- [Additional Reference: Operators are functions](https://helm.sh/docs/chart_template_guide/functions_and_pipelines/#operators-are-functions)
### IF-ELSE Syntax
```t
{{ if PIPELINE }}
  # Do something
{{ else if OTHER PIPELINE }}
  # Do something else
{{ else }}
  # Default case
{{ end }}
```

## Step-02: Review values.yaml
```yaml
# If, else if, else
myapp:
  env: prod
  retail:
    enableFeature: true
```

## Step-03: Logic and Flow Control Function: and 
- [Logic and Flow Control Functions](https://helm.sh/docs/chart_template_guide/function_list/#logic-and-flow-control-functions)
- **and:**  Returns the boolean AND of two or more arguments (the first empty argument, or the last argument).
```t
# and Syntax
and .Arg1 .Arg2
```
## Step-04: Implement if-else for replicas with Boolean 

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
  labels:
    app: nginx
spec:
{{- with .Values.myapp }}
{{- if and .retail.enableFeature (eq .env "prod") }}
  replicas: 6
{{- else if eq .env "prod" }}
  replicas: 4
{{- else if eq .env "qa" }}  
  replicas: 2
{{- else }}  
  replicas: 1  
{{- end }}
{{- end }}
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: ghcr.io/stacksimplify/kubenginx:4.0.0
        ports:
        - containerPort: 80
```

## Step-05: Verify if-else
```t
# Change to Chart Directory
cd helmbasics

# Helm Template 
helm template myapp1 . --set myapp.retail.enableFeature=true
helm template myapp1 . --set myapp.retail.enableFeature=false
helm template myapp1 . --set myapp.env=qa
helm template myapp1 . --set myapp.env=dev

# Helm Install Dry-run 
helm install myapp1 . --dry-run

# Helm Install
helm install myapp1 . --rollback-on-failure

# Verify Pods
helm status myapp1 --show-resources

# Uninstall Release
helm uninstall myapp1
```



# Helm Development - Variables

## Step-01: Introduction
- How to use Variables ?

## Step-02: Variables in Helm Templates
```yaml
# Change-1: Add Variable at the top of deployment template
{{- $chartname := .Chart.Name -}}

# Change-2: Add appHelmChart annotation with variable in deployment.yaml
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
        appManagedBy: {{ $.Release.Service }}
        appHelmChart: {{ $chartname }}        
      {{- end }}  

# Change to Chart Directory
cd helmbasics  

# Helm Template
helm template myapp101 .

# Helm Install with dry-run
helm install myapp101 . --dry-run  

# Observation:
We should see variable value substituted successfully
```

## Step-03: Test Variables in combination with Pipelines
```t
# Add Pipeline with quote and upper function
{{- $chartname := .Chart.Name | quote | upper -}}
apiVersion: apps/v1
kind: Deployment
metadata:

# Change to Chart Directory
cd helmbasics  

# Helm Template
helm template myapp101 .

# Helm Install with dry-run
helm install myapp101 . --dry-run  

# Helm Install with --rollback-on-failure
helm install myapp101 . --rollback-on-failure 

# List Helm Releases
helm list

# List Kubernetes Pods
kubectl get pods

# Helm get manifest
helm get manifest myapp101

# Helm Uninstall
helm uninstall myapp101
```

# Helm Development - Flow Control Range Action with List

## Step-01: Introduction
- Implement `Range` with `List of Values` from `values.yaml`
- Implement on how to call `Helm Variable` in Range loop
 
## Step-02: Implement "Range Action" with "List of Values"
- **Source Location:** backupfiles/namespace.yaml
- **Destication Location:** helmbasics/templates/namespace.yaml
- **File Name:** namespace.yaml
```t
# values.yaml
# Flow Control: Range with List
namespaces:
  - name: myapp1
  - name: myapp2
  - name: myapp3

# Range with List
{{- range .Values.namespaces }}
apiVersion: v1
kind: Namespace
metadata:
  name: {{ .name }}
---  
{{- end }}      

# Change to Chart Directory
cd helmbasics  

# Helm Template
helm template myapp1 .

# Helm Install with dry-run
helm install myapp1 . --dry-run 

# Helm Install and Test
helm install myapp1 . --rollback-on-failure
helm list

# Helm Status
helm status myapp1 --show-resources

# List k8s namespaces
kubectl get ns

# Observation:
We should see all the namespaces created

# Uninstall Helm Release
helm uninstall myapp1
```


## Step-03: Implement "Range Action" with "List of Values" with Variables
- **Source Location:** backupfiles/namespace-with-variable.yaml
- **Destication Location:** helmbasics/templates/namespace-with-variable.yaml
- **File Name:** namespace-with-variable.yaml
```t
# values.yaml
# Flow Control: Range with List and Helm Variables
environments:
  - name: dev
  - name: qa
  - name: uat  
  - name: prod    

# Range with List
{{- range $environment := .Values.environments }}
apiVersion: v1
kind: Namespace
metadata:
  name: {{ $environment.name }}
---  
{{- end }}           

# Change to Chart Directory
cd helmbasics  

# Helm Template
helm template myapp1 .

# Helm Install with dry-run
helm install myapp1 . --dry-run 

# Helm Install and Test
helm install myapp1 . --rollback-on-failure
helm list

# Helm Status
helm status myapp1 --show-resources

# List k8s namespaces
kubectl get ns

# Observation:
We should see all the namespaces created

# Uninstall Helm Release
helm uninstall myapp1
```


# Helm Development - Flow Control Range with Dictionary

## Step-01: Introduction
- Implement Range with Map or Dictionary from `values.yaml`
- Implement on how to call `Helm Variable` in Range loop

## Step-02: Range with Key Value pairs or Map or Dictionary 
- **Source Location:** backupfiles/namespace.yaml
- **Destication Location:** helmbasics/templates/namespace.yaml
- **File Name:** namespace.yaml
```yaml
# values.yaml
# Range with Dictionary
myapps:
  config1: 
    appName: myapp1
    appType: webserver
    appTech: HTML
    appDb: mysql
  config2: 
    appName: myapp2
    appType: webserver
    appTech: HTML
    appDb: mysql
  
# Range with Dictionary
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}-configmap1
data: 
{{- range $key, $value := .Values.myapps.config1 }}
{{- $key | nindent 2}}: {{ $value }}
{{- end}}  

# Change to Chart Directory
cd helmbasics  

# Helm Template
helm template myapp1 .

# Helm Install with dry-run
helm install myapp1 . --dry-run 

# Helm Install and Test
helm install myapp1 . --rollback-on-failure
helm list

# Helm Status
helm status myapp1 --show-resources

# List k8s namespaces
kubectl get configmap
kubectl get configmap <NAME-OF-CONFIGMAP> -o yaml
kubectl get configmap myapp1-helmbasics-configmap1 -o yaml

# Observation:
We should see configmap with key value pairs

# Uninstall Helm Release
helm uninstall myapp1
```


## Step-03: Range - Access Builtin Object from Root inside Range using Helm  Variable
- **Source Location:** backupfiles/namespace-with-variable.yaml
- **Destication Location:** helmbasics/templates/namespace-with-variable.yaml
- **File Name:** namespace-with-variable.yaml
```yaml
# values.yaml
# Range with Dictionary
myapps:
  config1: 
    appName: myapp1
    appType: webserver
    appTech: HTML
    appDb: mysql
  config2: 
    appName: myapp2
    appType: webserver
    appTech: HTML
    appDb: mysql
  
# Range: Access Root Object in Range with Helm Variable
{{- $chartName := .Chart.Name  }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}-configmap2
data: 
{{- range $key, $value := .Values.myapps.config2 }}
{{- $key | nindent 2}}: {{ $value }}-{{ $chartName }}
{{- end}}  

# Change to Chart Directory
cd helmbasics  

# Helm Template
helm template myapp1 .

# Helm Install with dry-run
helm install myapp1 . --dry-run 

# Helm Install and Test
helm install myapp1 . --rollback-on-failure
helm list

# List k8s namespaces
kubectl get configmap
kubectl get configmap <NAME-OF-CONFIGMAP> -o yaml
kubectl get configmap myapp1-helmbasics-configmap2 -o yaml

# Observation:
We should see configmap with key value pairs

# Uninstall Helm Release
helm uninstall myapp1
```



# Helm Development - Named Templates

## Step-01: Introduction
- Create Named Template
- Call the named template using template action
- Pass Root Object dot (.) to template action provided if we are using Helm builtin objects in our named template
- For `template call` use `pipelines` and see if it works
- Replace `template call` with special purpose function `include` in combination with `pipelines` and test it


## Step-02: Create a Named Template
- **File Location:** deployment.yaml
- Define the below named template in `deployment.yaml`
```t
{{/* Common Labels */}}
{{- define "helmbasics.labels"}}
    app: nginx
{{- end }}
```

## Step-03: Call the named template using template action
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}-deployment 
  labels:
  {{- template "helmbasics.labels" }}
```

## Step-04: Test the output with template action
```t
# Change to Chart Directory 
cd helmbasics

# Helm Template Command
helm template myap101 .

# Helm Install with dry-run command
helm install myapp101 . --dry-run

# Helm Release
helm install myapp101 . --rollback-on-failure
kubectl get deploy
kubectl describe deploy <DEPLOYMENT-NAME>
helm uninstall myapp101
```

## Step-05: Add one Builtin Object Chart.Name to labels
```t
{{/* Common Labels */}}
{{- define "helmbasics.labels"}}
    app: nginx
    chartname: {{ .Chart.Name }}
{{- end }}
```

## Step-06: Test the output with template action
```t
# Change to Chart Directory 
cd helmbasics

# Helm Template Command
helm template myap101 .

# Helm Install with dry-run command
helm install myapp101 . --dry-run
Observation:
1. Chart name filed should be empty
2. Chart Name was not in the scope for our defined template.
3. When a named template (created with define) is rendered, it will receive the scope passed in by the template call. 
4. No scope was passed in, so within the template we cannot access anything in "."
5. This is easy to fix. We simply pass a scope to the template
```

## Step-07: Pass scope to the template call
- Add dot "." (Root Object or period) at the end of template call to pass scope to template call
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}-deployment # Action Element
  labels:
  {{- template "helmbasics.labels" . }}
```

## Step-08: Test the output with template action when scope passed to template call
```t
# Change to Chart Directory 
cd helmbasics

# Helm Template Command
helm template myap101 .

# Helm Install with dry-run command
helm install myapp101 . --dry-run
Observation:
Chart Name should be displayed
```

## Step-09: Pipe an Upper function to template 
```t
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}-deployment # Action Element
  labels:
  {{- template "helmbasics.labels" . | upper }}
```

## Step-10: Test the output when template action + pipe + upper function
```t
# Change to Chart Directory 
cd helmbasics

# Helm Template Command
helm template myap101 .

# Helm Install with dry-run command
helm install myapp101 . --dry-run
Observation:
1. Should fail with error. What is the reason for failure ?
2. Template is an action, and not a function, there is no way to pass the output of a template call to other functions; 
```

## Step-11: Replace Template action with Special Purpose include function
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}-deployment # Action Element
  labels:
  {{- include "helmbasics.labels" . | upper }}
```

## Step-10: Test the output include function
```t
# Change to Chart Directory 
cd helmbasics

# Helm Template Command
helm template myap101 .

# Helm Install with dry-run command
helm install myapp101 . --dry-run
Observation:
1. Call include "helmbasics.labels" -- should be successful
2. Should show all labels in upper case
```
## Step-11: Underscoe file (_helpers.tpl)
- Move the named template `helmbasics.labels` to `_helpers.tpl` file
- But files whose name begins with an underscore (_) are assumed to not have a kubernetes manifest inside. 
- These files are not rendered to Kubernetes object definitions, but are available everywhere within other chart templates for use.
- These files are used to store partials and helpers. 
```t
{{/* Common Labels */}}
{{- define "helmbasics.labels"}}
    app: nginx
    chartname: {{ .Chart.Name }}
{{- end }}
```

## Step-12: Test the output after moving named template to _helpers.tpl
```t
# Change to Chart Directory 
cd helmbasics

# Helm Template Command
helm template myap101 .

# Helm Install with dry-run command
helm install myapp101 . --dry-run
Observation:
1. call include "helmbasics.labels" -- should be successful
2. Should show all labels in upper case
```


# Helm Printf Function

## Step-01: Introduction
- **[printf](https://helm.sh/docs/chart_template_guide/function_list/#printf):** Returns a string based on a formatting string and the arguments to pass to it in order.


## Step-02: Create a Named Template with printf function
```t
{{/* Kubernetes Resource Name: String Concat with Hyphen */}}
{{- define "helmbasics.resourceName" }}
{{- printf "%s-%s" .Release.Name .Chart.Name }}
{{- end }}
```

## Step-03: Call the named template in deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "helmbasics.resourceName" . }}-deployment 
  labels:
```

## Step-04: Test the changes
```t
# Change to Chart Directory 
cd helmbasics

# Helm Template Command
helm template myapp1 .

# Helm Install with dry-run command
helm install myapp1 . --dry-run

# Helm Install with --rollback-on-failure flag
helm install myapp1 . --rollback-on-failure

# Helm Uninstall
helm uninstall myapp1
```

# Helm Named Templates - Call Template in Template

## Step-01: Introduction
- We can call one named template in other named template.

## Step-02: Update _helpers.tpl 
- We will udpate the template `helmbasics.labels` with `template-in-template` as additional label by calling the named template `helmbasics.resourceName`
```t
{{/* Common Labels */}}
{{- define "helmbasics.labels"}}
    app.kubernetes.io/managed-by: helm
    app: nginx
    chartname: {{ .Chart.Name }}
    template-in-template: {{ include "helmbasics.resourceName" . }}
{{- end }}
```

## Step-03: Test the changes
```t
# Change to Chart Directory 
cd helmbasics

# Helm Template Command
helm template myapp1 .

# Helm Install with dry-run command
helm install myapp1 . --dry-run

# Helm Install with --rollback-on-failure flag
helm install myapp1 . --rollback-on-failure

# Helm Uninstall
helm uninstall myapp1
```


# Create and Package Helm Charts

## Step-01: Introduction
1. We will learn the following things
2. helm create to create a new Helm Chart
3. Update the Chart with basic information like our Docker Image, appversion, chart version 
4. Update the Chart to support to NodePort Service, helm install and test
5. helm package 
6. helm package --app-version --version
- [Docker Image used](https://github.com/users/stacksimplify/packages/container/package/kubenginx)

## Step-02: Helm Create Chart
```t
# Helm Create Chart
helm create <CHART-NAME>
helm create myfirstchart
Observation: 
1. It will create a base Helm Chart template 
2. We can call it as a starter chart. 
```

## Step-03: Update values.yaml with our Application Docker Image
- [Docker Image used](https://github.com/users/stacksimplify/packages/container/package/kubenginx)
- Review `templates/deployment.yaml`
```yaml
image:
  repository: ghcr.io/stacksimplify/kubenginx
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: ""
```
## Step-04: Convert the Kubernetes Service to NodePort
```yaml
# Update values.yaml
service:
  type: NodePort
  port: 80 
  nodePort: 31231

# Update templates/service.yaml
nodePort: {{ .Values.service.nodePort }}
```

## Step-05: Update Chart.yaml
```t
### Chart Version and Description
# Before
version: 0.1.0
description: A Helm chart for Kubernetes

# After
version: 1.0.0
description: A Helm Chart with NodePort Service

### appVersion
# Before
appVersion: "1.16.0"

# After (update our Docker Image tag version)
appVersion: "1.0.0"
```

## Step-06: Helm Install - Chart Version 1.0.0 and Test it
```t
# Helm Install
cd myfirstchart
helm install myapp1v1 .

# List Helm Releases
helm list
helm list --output=yaml

# Helm Status
helm status myapp1v1 --show-resources

# Using kubectl commands
kubectl get pods
kubectl get svc

# Access in Browser
http://127.0.0.1:31231
http://localhost:31231
```
## Step-07: Helm Package - v1.0.0
```t
# Check if you are  in Directory
25-Helm-Create-and-Package-Chart

# Helm Package
helm package myfirstchart/ --destination packages/
or
helm package myfirstchart/ -d packages/

# Review Package file
cd pakcages
ls -lrta
Package file name: myfirstchart-1.0.0.tgz
```

## Step-08: Helm Package - v2.0.0
```t
### Chart Version and Description
# Before
version: 1.0.0
description: A Helm Chart with NodePort Service

# After
version: 2.0.0
description: A Helm Chart with NodePort Service

### appVersion
# After (update our Docker Image tag version)
appVersion: "1.0.0"

# After (update our Docker Image tag version)
appVersion: "2.0.0"

# Helm Package
helm package myfirstchart/ --destination packages/
helm package myfirstchart/ -d packages/

# Review Package file
cd pakcages
ls -lrta
Package file name: myfirstchart-1.0.0.tgz
Package file name: myfirstchart-2.0.0.tgz
```

## Step-09: Helm Install by path to a packaged chart and Verify
```t
# Helm Install
helm install myapp1v2 packages/myfirstchart-2.0.0.tgz --set service.nodePort=31232

# Using kubectl commands
kubectl get pods
kubectl get svc

# List Helm Releases
helm list
helm list --output=yaml

# Helm Status
helm status myapp1v2 --show-resources

# Access in Browser
http://127.0.0.1:31232
http://localhost:31232
```

## Step-10: Helm Package with --app-version, --version
- [Docker Image used](https://github.com/users/stacksimplify/packages/container/package/kubenginx)
```t
# Helm Package  --app-version
helm package myfirstchart/ --app-version "3.0.0" --version "3.0.0" --destination packages/
```

## Step-11: Helm Install and Test if --version "3.0.0" worked
```t
# Helm Install from package
helm install myapp1v3 packages/myfirstchart-3.0.0.tgz --set service.nodePort=31233

# Using kubectl commands
kubectl get pods
kubectl get svc

# List Helm Releases
helm list
helm list --output=yaml

# Helm Status
helm status myapp1v3 --show-resources

# Access in Browser
http://127.0.0.1:31233
http://localhost:31233
Observation:
1. We can see V3 version of Application 
```

## Step-12: Uninstall Helm Releases
```t
# List Helm Releases
helm list
helm list --output=yaml

# Uninstall Helm Releases
helm uninstall myapp1v1
helm uninstall myapp1v2
helm uninstall myapp1v3
```
## Step-13: Helm Show Commands
- **helm show:** show information of a chart
```t
# Helm Show Chart
helm show chart myfirstchart/
helm show chart packages/myfirstchart-2.0.0.tgz

# Helm Show Values
helm show values myfirstchart/
helm show values packages/myfirstchart-2.0.0.tgz

# Helm Show readme
helm show readme myfirstchart/

# Helm Show All
helm show all myfirstchart/
helm show all packages/myfirstchart-2.0.0.tgz
```

```
kubectl get service 
NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes              ClusterIP   10.96.0.1       <none>        443/TCP        18d
myapp1v1-myfirstchart   NodePort    10.110.32.254   <none>        80:31231/TCP   16s


kubectl port-forward svc/myapp1v1-myfirstchart 8080:80 creates a temporary tunnel from your laptop to that Kubernetes service.
Meaning of each part:
- kubectl: Kubernetes CLI
- port-forward: forward traffic from your machine into the cluster
- svc/myapp1v1-myfirstchart: target the Service named myapp1v1-myfirstchart
- 8080:80: map local port 8080 to service port 80
So after running it:
- you open http://localhost:8080
- traffic goes from your Mac to kubectl
- kubectl forwards it into the cluster
- the Service then sends it to the backing pod on port 80
Why this helps:
- it bypasses Docker Desktop NodePort host-network issues
- it gives you a guaranteed local endpoint on localhost
Notes:
- the command keeps running in that terminal while forwarding is active
- stop it with Ctrl+C
- if 8080 is busy, use another local port, for example:
kubectl port-forward svc/myapp1v1-myfirstchart 9090:80
Then browse to:
http://localhost:9090
```



# Helm Subcharts - Dependency Command

## Step-01: Introduction
- Create Parent Chart
- helm dependency list
- helm dependency update
- helm dependency build
- helm dependency version constraints
- helm dependency repository @REPO vs REPO-URL

## Step-02: Create Parent Chart
```t
# Create Parent Chart
helm create parentchart
```

## Step-03: Update Helm Dependencies in Parent Chart Chart.yaml
```yaml
apiVersion: v2
name: parentchart
description: A Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "1.16.0"
dependencies:
- name: mychart1
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
- name: mychart2
  version: "0.4.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
- name: mysql
  version: "9.9.0"
  repository: "https://charts.bitnami.com/bitnami"
```

## Step-04: Helm Dependency Commands - List and Update
- **helm dependency list:** List all of the dependencies declared in a chart.
- **helm dependency update:** update parent chart `charts/` folded based on the contents of file `Chart.yaml`
```t
# Helm Dependency List
helm dependency list
Observation: 
You should see status "missing" because we still didnt do helm dependency update

# Verify Charts folder in parentchart
ls parentchart/charts
Observation: it should be empty. Dependency subcharts not downloaded

# Helm Dependency Update
helm dependency update CHART-NAME
helm dependency update parentchart/
ls parentchart/charts
Observation: 
1. We should see both charts (mychart1-0.1.0.tgz, mychart2-0.4.0.tgz, mysql-9.9.0.tgz)downloaded to "parentchart/charts" folder
2. We should see "Chart.lock" file in "parentchart" folder

# Review Chart.lock file
cat parentchart/Chart.lock 

# Helm Dependency list
helm dependency list parentchart/
Observation: Should see status as "OK"
```

## Step-05: Helm Dependency Chart Version Ranges
- Updates to parent chart `Chart.yaml`

### Step-05-01: Helm Chart Version Notation
```t
Helm Chart Version Notation: Major.Minor.Patch 
MySQL Helm Chart Version: 9.10.8
Major: 9
Minor: 10
Patch: 8
```
### Step-05-02: Basic Comparison Operators
- We can define the version constraints using basic comparison operators
- Where possible, use version ranges instead of pinning to an exact version.
```t
# Basic Comparison Operators
version: "= 9.10.8" 
version: "!= 9.10.8" 
version: ">= 9.10.8"
version: "<= 9.10.8"
version: "> 9.10.8"   
version: "< 9.10.8"
version: ">= 9.10.8 < 9.11.0"  
```

### Step-05-03: For Range Comparison Major: Caret Symbol(ˆ)
- `x` is a placeholder
- The caret (^) operator is for major level changes once a stable (1.0.0) release has occurred.
```t
# For Range Comparison Major: Caret Symbol(ˆ)
^9.10.1  is equivalent to >= 9.10.1, < 10.0.0
^9.10.x  is equivalent to >= 9.10.0, < 10.0.0   
^9.10    is equivalent to >= 9.10, < 10
^9.x     is equivalent to >= 9.0.0, < 10        
^0       is equivalent to >= 0.0.0, < 1.0.0
```

### Step-05-05: For Range Comparison Minor: Tilde Symbol(~)
- `x` is a placeholder
- The tilde (~) operator is for 
  - patch level ranges when a minor version is specified 
  - major level changes when the minor number is missing. 
- The suggested default is to use a patch-level version match which is first one in the below table 
```t
# For Range Comparison Major: Caret Symbol(ˆ)
~9.10.1  is equivalent to >= 9.10.1, < 9.11.0 # Patch-level version match
~9.10    is equivalent to >= 9.10, < 9.11
~9       is equivalent to >= 9, < 10
^9.x     is equivalent to >= 9.0.0, < 10        
^0       is equivalent to >= 0.0.0, < 1.0.0
```
### Step-05-06: Verify with some examples
```yaml
dependencies:
- name: mysql
  version:" "9.10.9"
  #version: ">=9.10.1" # Should dowload latest version available as on that day
  #version: "<=9.10.6" # Should download 9.10.6 mysql helm chart package
  #version: "~9.9.0" # Should download latest from 9.9.x (Patch version) 
  #version: "~9.9" # Should download latest from 9.9 
  #version: "~9" # Should download latest from 9.x 
  repository: "https://charts.bitnami.com/bitnami"


# helm dependency update
helm dependency update
or
helm dep update  
```

## Step-06: Helm Dependency Build Command
- **helm dependency build:** rebuild the `charts/` directory based on the `Chart.lock` file
- In short `dep update` command will negotiate with version constraints defined in `Chart.yaml` where as `dep build` will try to build or download or update whatever version preset in `Chart.lock` file
- If no lock file is found, `helm dependency build` will mirror the behavior of `helm dependency update`.
```t
# helm dependency build
helm dependency build CHART-NAME
helm dependency build parentchart
```

## Step-07: Helm Dependency Repository @REPO vs REPO-URL
- When we are using Helm with DevOps pipelines across environments "@REPO" approach is not recommended
- REPO-URL approach (repository: "https://charts.bitnami.com/bitnami") is always recommended
```t
# With Repository URL (Recommended approach)
dependencies:
- name: mysql
  version: ">=9.10.8"
  repository: "https://charts.bitnami.com/bitnami"

# List Helm Repo
helm repo list
helm search repo bitnami/mysql --versions

# With @REPO (local repo reference - NOT RECOMMENDED)
dependencies:
- name: mysql
  version: ">=9.10.8"
  repository: "@bitnami"

# Clean-Up Charts folder and Chart.lock
rm parentchart/charts/*
rm parentchart/Chart.lock

# Ensure we are using repository: "@bitnami"
helm dependency update
ls parentchart/charts/
cat parentchart/Chart.lock
Observation: Should work as expected
```


# Helm Dependency - Alias

## Step-01: Introduction
- Condition
- Alias
- Override subchart(child chart) values from parent chart

## Step-02: Update Parentchart CIP to NodePort Service
```yaml
# values.yaml
service:
  type: NodePort
  port: 80
```

## Step-03: Chart.yaml
- Understand the importance of `alias` when defining dependencies
```yaml
apiVersion: v2
name: parentchart
description: Learn Helm Dependency Concepts
type: application
version: 0.1.0
appVersion: "1.16.0"
dependencies:
- name: mychart4
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart4dev
- name: mychart4
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart4qa  
- name: mychart2
  version: "0.4.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart2
```

## Step-04: Deploy and Test
```t
# Helm Dependency Update
helm dependency update parentchart/
or
helm dep update parentchart/

# Helm Install
helm install myapp1 parentchart/ --rollback-on-failure

# Helm List
helm list

# Helm Status
helm status myapp1 --show-resources

# List Deployments
kubectl get deploy

# List Pods
kubectl get pods

# List Services
kubectl get svc

# Access Application
parentchart: http://localhost:<port-from-get-svc-output>
childchart4dev: http://localhost:<port-from-get-svc-output>
childchart4qa: http://localhost:<port-from-get-svc-output>
mychart2: http://localhost:31232
```

## Step-05: Uninstall Helm Release
```t
# Helm Uninstall
helm uninstall myapp1
```

# Helm Dependency - Condition

## Step-01: Introduction
- Implement `Condition` for enabling or disabling Sub Charts or Child Charts
- Override subchart(child chart) values from parent chart


## Step-02: Chart.yaml
- Understand the importance of `condition` when defining dependencies
- By default, if we the condition is defined or not `condition: mychart4.enabled`, chart is enaled when defined
- To disable it we need to explicitly make it `false` in `values.yaml`
```yaml
dependencies:
- name: mychart4
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart4
  condition: mychart4.enabled
- name: mychart2
  version: "0.4.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart2
  condition: mychart2.enabled
```

## Step-03: Deploy and Test - By Default enabled is true
```t
# Helm Dependency Update
helm dependency update parentchart/
or
helm dep update parentchart/

# Helm Install
helm install myapp1 parentchart/ --rollback-on-failure

# Helm List
helm list

# Helm Status
helm status myapp1 --show-resources

# List Deployments
kubectl get deploy

# List Pods
kubectl get pods

# List Services
kubectl get svc

# Access Application
parentchart: http://localhost:<port-from-get-svc-output>
mychart4: http://localhost:<port-from-get-svc-output>
mychart2: http://localhost:31232

# Helm Uninstall
helm uninstall myapp1
```

## Step-04: Update values.yaml
```yaml
# Values for Child Charts with Chart Name
mychart4:
  enabled: false
mychart2:
  enabled: false  
```


## Step-05: Deploy and Test - when childcharts are disabled
```t
# Helm Dependency Update
helm dependency update parentchart/
or
helm dep update parentchart/

# Helm Install
helm install myapp1 parentchart/ --rollback-on-failure

# Helm List
helm list

# Helm Status
helm status myapp1 --show-resources

# List Deployments
kubectl get deploy
Observation:
1. Child Charts will not be deployed.
2. No k8s resources for child charts will be created

# List Pods
kubectl get pods

# List Services
kubectl get svc

# Access Application
parentchart: http://localhost:<port-from-get-svc-output>
```

## Step-06: Uninstall Helm Release
```t
# Helm Uninstall
helm uninstall myapp1
```

# Helm Dependency - Condition with Alias

## Step-01: Introduction
- Implement `Condition` for enabling or disabling Sub Charts or Child Charts
- Override subchart(child chart) values from parent chart


## Step-02: Chart.yaml
- If we have multiple dependencies with same chart name `mychart4` with different alias names like `childchart4dev` and `childchart4qa` in this case we need to define values.yaml with `alias names` for enabling or disabling those sub charts
```yaml
apiVersion: v2
name: parentchart
description: Learn Helm Dependency Concepts
type: application
version: 0.1.0
appVersion: "1.16.0"
dependencies:
- name: mychart4
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart4dev
  condition: childchart4dev.enabled
- name: mychart4
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart4qa
  condition: childchart4qa.enabled  
- name: mychart2
  version: "0.4.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart2
  condition: childchart2.enabled
```

## Step-03: Update values.yaml
- Here only `childchart4qa` so only k8s resources for that chart should created in addition to parent chart resources
```yaml
# Values for Child Charts with Alias Name of Chart
childchart4dev:
  enabled: false 
childchart4qa:
  enabled: true   
childchart2:
  enabled: false 
```


## Step-04: Deploy and Test 
```t
# Helm Dependency Update
helm dependency update parentchart/
or
helm dep update parentchart/

# Helm Install
helm install myapp1 parentchart/ --rollback-on-failure

# Helm List
helm list

# Helm Status
helm status myapp1 --show-resources

# List Deployments
kubectl get deploy
Observation:
1. Resources for childchart4qa should be created in addition to parent chart

# List Pods
kubectl get pods

# List Services
kubectl get svc

# Access Application
parentchart: http://localhost:<port-from-get-svc-output>
childchart4qa: http://localhost:<port-from-get-svc-output>
```

## Step-05: Uninstall Helm Release
```t
# Helm Uninstall
helm uninstall myapp1
```

# Helm Dependency - Using Tags

## Step-01: Introduction
- Instead of using `condition` we are going to use `tags`
- If we have more amount of subcharts that need to be divided in to groups then we need to use `tags` instead of `condition`

 ## Step-02: Review Chart.yaml
 - Instead of using `condition` we are going to use `tags`
```yaml
apiVersion: v2
name: parentchart
description: Learn Helm Dependency Concepts
type: application
version: 0.1.0
appVersion: "1.16.0"
dependencies:
- name: mychart4
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart4dev
  #condition: childchart4dev.enabled
  tags: 
    - frontend 
- name: mychart4
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart4qa1
  #condition: childchart4qa.enabled
  tags: 
    - frontend   
- name: mychart4
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart4qa2
  #condition: childchart4qa2.enabled
  tags: 
    - frontend        
- name: mychart2
  version: "0.4.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  alias: childchart2
  #condition: childchart2.enabled
  tags: 
    - backend
 ```

 ## Step-03: Usecase-1: Both frontend and backend false
 ```t
 # Usecase-1: Both frontend and backend false
 # values.yaml
tags:
  frontend: false
  backend: false

# Helm Install
helm install myapp1 parentchart/ --rollback-on-failure

# List Pods
kubectl get pods
Observation:
1.  We should see only 1 pod (parentchart) pod running
```


 ## Step-04: Usecase-2: Backend True and Frontend false
 ```t
# Helm Install
helm upgrade myapp1 parentchart/ --rollback-on-failure --set tags.backend=true

# List Pods
kubectl get pods
Observation:
1.  We should see 2 pods (parentchart and childchart2) running
```

 ## Step-05: Usecase-2: Backend True and Frontend True
 ```t
# Helm Install
helm upgrade myapp1 parentchart/ --rollback-on-failure --set tags.backend=true --set tags.frontend=true

# List Pods
kubectl get pods
Observation:
1.  We should see 5 pods (parentchart, childchart2, childchart4dev, childchart4qa1, childchart4qa2) running
```

## Step-06: Uninstall Helm Charts
```t
# Helm Uninstall
helm uninstall myapp1
```


# Helm Dependency - Override Subchart Values

## Step-01: Introduction
- Override subchart(child chart) values from parent chart


## Step-02: Review Chart.yaml
```yaml
apiVersion: v2
name: parentchart
description: Learn Helm Dependency Concepts
type: application
version: 0.1.0
appVersion: "1.16.0"
dependencies:
- name: mychart4
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  condition: mychart4.enabled
- name: mychart2
  version: "0.4.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
  condition: mychart2.enabled
```

## Step-03: Review mychart4, mychart2 subchart replicaCount value
```t
# Change Directory
cd 31-Helm-Dependency-Override-Subchart-Values

# Review mychart4 Values from Helm package 
helm show values parentchart/charts/mychart4-0.1.0.tgz

# Review mychart2 Values from Helm package  
helm show values parentchart/charts/mychart2-0.4.0.tgz 
```

## Step-04: Update values.yaml
- Override `replicaCount` value in subcharts from parent chart `values.yaml`
```yaml
# Values for Child Charts with Chart Name
mychart4:
  enabled: true
  replicaCount: 3
mychart2:
  enabled: true  
  replicaCount: 3
```

## Step-05: Deploy and Test 
```t
# Helm Dependency Update
helm dependency update parentchart/
or
helm dep update parentchart/

# Helm Install
helm install myapp1 parentchart/ --rollback-on-failure

# Helm List
helm list

# Helm Status
helm status myapp1 --show-resources

# List Deployments
kubectl get deploy

# List Pods
kubectl get pods
Observation:
1. We should see 3 pods for each child chart
2. 1 pod for parentchart
3. We have successfully overrided the child chart values from parentchart values.yaml

# List Services
kubectl get svc

# Access Application
parentchart: http://localhost:<port-from-get-svc-output>
mychart4: http://localhost:<port-from-get-svc-output>
mychart2: http://localhost:31232
```

## Step-06: Uninstall Helm Release
```t
# Helm Uninstall
helm uninstall myapp1
```

# Helm Sub Charts - Use Global Values in Sub Charts
## Step-01: Introduction
- Managing Dependencies manually
- Define Global Values

## Step-02: Review Chart.yaml
```yaml
apiVersion: v2
name: parentchart
description: Learn Helm Dependency Concepts
type: application
version: 0.1.0
appVersion: "1.16.0"
dependencies:
- name: mychart4
  version: "0.1.0"
  repository: "file://charts/mychart4"
  alias: childchart4
  tags: 
    - frontend
- name: mychart2
  version: "0.4.0"
  repository: "file://charts/mychart2"
  alias: childchart2
  tags: 
    - backend
```

## Step-03: Pull charts using helm pull command 
- We are going to pull the charts to `parentchart/charts` directory using `helm pull` command
- Also ensure that those packages are untarred or unzipped
```t
# Change Directory
cd parentchart/charts

# Helm Pull MyChart4
helm pull https://stacksimplify.github.io/helm-charts/mychart4-0.1.0.tgz --untar

# Helm Pull MyChart2
helm pull https://stacksimplify.github.io/helm-charts/mychart2-0.4.0.tgz --untar

# Remove package files .tgz files
rm -rf *.tgz
```

## Step-04: To Build or Package Sub Charts
```t
# Change to Chart Directory
cd parentchart

# Helm Dependency list
helm dependency list

## Sample Outout
Kalyans-MacBook-Pro:parentchart kalyan$ helm dependency list
NAME    	VERSION	REPOSITORY             	STATUS  
mychart4	0.1.0  	file://charts/mychart4 	unpacked
mychart2	0.4.0  	file://charts/mychart2	unpacked

# Helm Dependency Update / Build
helm dependency update

# Review charts folder
ls charts/
Observation: you should find *.tgz files for both charts

> # helm dep list should show status as OK
Kalyans-MacBook-Pro:parentchart kalyan$ helm dep list
NAME    	VERSION	REPOSITORY            	STATUS
mychart4	0.1.0  	file://charts/mychart4	ok    
mychart2	0.4.0  	file://charts/mychart2	ok  


# Delete subchart tgz files
rm charts/*.tgz
```

## Step-05: Define Global value in Parent Chart values.yaml
- **File:** parentchart/values.yaml
```yaml
# Define Global Values
global:
  replicaCount: 4
```

## Step-06: Update Parent Chart and Sub Chart deployment.yaml
- **File:** parentchart/templates/deployment.yaml
- **File:** charts/mychart4/templates/deployment.yaml
- **File:** charts/mychart2/templates/deployment.yaml
```yaml
replicas: {{ .Values.global.replicaCount }}
```

## Step-07: Test Global Values
```t
# Change to Chart Directory
cd parentchart

# Helm Install
helm install myapp1 . --rollback-on-failure

# Verify Pods for all 3 charts
kubectl get pods
Observation: 
All 3 charts should spin 4 pods per each based on ".Values.global.replicaCount=4"

# helm uninstall
helm uninstall myapp1
```


# Helm Dependency - Import Values Explicit

## Step-01: Introduction
- Import Values Explicit

## Step-02: Review / Update Subchart values.yaml
- **File Location:** parentchart/charts/mychart1/values.yaml
```yaml
# Export Values - MyChart1 (Used for Import Values Explicit Usecase)
exports:
  mychart1Data:
    mychart1appInfo:
      appName: kapp1
      appType: MicroService
      appDescription: Used for listing products    
```

## Step-03: Review / Update Chart.yaml mychart1 dependency with import-values argument
```yaml
- name: mychart1
  version: "0.1.0"
  repository: "file://charts/mychart1"
  alias: childchart1
  tags: 
    - frontend
  import-values:
    - mychart1Data # Explicit Values Import Usecase
```

## Step-04: Review / Update parentchart configmap.yaml
- **File Location:** parentchart/templates/configmap.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name:  {{ include "parentchart.fullname" . }}-import-explicit
data:
{{- toYaml .Values.mychart1appInfo | nindent 2 }}
```

## Step-05: Import Values Explicit: Deploy and Verify 
```t
# Change to Chart Directory
cd parentchart

# Helm Install
helm install myapp1 . --rollback-on-failure

# Helm List
helm list

# Helm Status
helm status myapp1 --show-resources

# List k8s Deployments
kubectl get deploy

# List k8s pods
kubectl get pods

# List k8s ConfigMaps
kubectl get cm
kubectl get cm myapp1-parentchart-import-explicit -o yaml
Observation:
We should see the data exported from parentchart/charts/mychart1/values.yaml imported successfully to configmap in parentchart. 

# Helm Uninstall
helm uninstall myapp1 
```

## Step-06: Test when mychart1 is disabled 
```t
# Change to Chart Directory
cd parentchart

# Helm Install
helm install myapp1 . --rollback-on-failure --set tags.frontend=false

# Review Configmap
kubectl get cm myapp1-parentchart-import-explicit -o yaml
Observation:
1. We should not see any data for configmap

# Helm Uninstall
helm uninstall myapp1
```


# Helm Dependency - Import Values Implicit

## Step-01: Introduction
- Implement Import Values Implicit usecase

## Step-02: Review / Update parentchart Chart.yaml
- **File Location:** parentchart/Chart.yaml
- Define `import-values`
```yaml
apiVersion: v2
name: parentchart
description: Learn Helm Dependency Concepts
type: application
version: 0.1.0
appVersion: "1.16.0"
dependencies:
- name: mychart1
  version: "0.1.0"
  repository: "file://charts/mychart1"
  alias: childchart1
  tags: 
    - frontend

- name: mychart2
  version: "0.4.0"
  repository: "file://charts/mychart2"
  alias: childchart2
  tags: 
    - backend
  import-values: # Implicit Values Usecase
    - child: service 
      parent: mychart2service   
    - child: image 
      parent: mychart2image      
```

## Step-03: Review / Update parentchart configmap.yaml
- **File Location:** parentchart/templates/configmap.yaml
- Use imported values in `configmap.yaml`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name:  {{ include "parentchart.fullname" . }}-import-implicit
data:
  serviceType: {{ .Values.mychart2service.type }}
  servicePort: {{ .Values.mychart2service.port | quote}}
  servicenodePort: {{ .Values.mychart2service.nodePort | quote }}
  imageRepository: {{ .Values.mychart2image.repository }}
```


## Step-04: Import Values Implicit: Deploy and Verify 
```t
# Change to Chart Directory
cd parentchart

# Helm Install
helm install myapp1 . --rollback-on-failure

# Helm List
helm list

# Helm Status
helm status myapp1 --show-resources

# List k8s Deployments
kubectl get deploy

# List k8s pods
kubectl get pods

# List k8s ConfigMaps
kubectl get cm
kubectl get cm myapp1-parentchart-import-implicit -o yaml
Observation:
We should see the data exported from parentchart/charts/mychart2/values.yaml imported successfully to configmap in parentchart. 

# Helm Uninstall
helm uninstall myapp1 
```

## Step-06: Test when mychart2 is disabled 
```t
# Change to Chart Directory
cd parentchart

# Helm Install (When mychart2 is disabled)
helm install myapp1 . --rollback-on-failure --set tags.backend=false
Observation:
Should fail with error 

## Error
Kalyans-Mac-mini:parentchart kalyanreddy$ helm install myapp1 . --rollback-on-failure --set tags.backend=false
Error: INSTALLATION FAILED: template: parentchart/templates/configmap.yaml:6:25: executing "parentchart/templates/configmap.yaml" at <.Values.mychart2service.type>: nil pointer evaluating interface {}.type
```


# Helm Starters

## Step-01: Introduction
- We are going to learn about Helm Starter Charts
- Create / Build a Starter Chart
- Using starter chart build a base chart

## Step-02: Helm Starter Charts
### What are Helm Starter Charts ?
1. Starter charts are same as regular Helm Charts
2. Starter charts are reusable template that helps us in building new charts. 
3. A new developer don't need to start from scratch in your organization if you already have starter charts. He can use them and build on top of it. 
4.  We can also enforce certain resources that needs to be available in the created charts.
### Where do we place the starter charts ?
5. We need to place starter charts in folder "$HELM_DATA_HOME/starters" folder
### Are there any drawbacks ?
6. The `Chart.yaml` will be overwritten by the generator.
7. Due to that we don't get the version or dependency charts from the starter chart template.

## Step-03: Create a Simple Helm Chart and Modify to a Starter Chart
- This step is completely optional for you.
- You will have `mystarterchart` folder ready for you to move on with next steps in the demo.
```t
# Helm Create
helm create mystarterchart

# Important Note
1. We are going to modify the default helm chart when we create it using "helm create" to very simpler one with only "deployment.yaml" and "service.yaml"

# Changes in Templates folder
1. Delete "tests" folder
2. Delete hpa.yaml, ingress.yaml and serviceaccount.yaml
3. Update "_helpers.tpl" to remove "serviceAccountName" template
4. In values.yaml, remove serviceaccount, ingress and autoscaling values
5. In values.yaml, update the service to NodePort with port as 31239
6. In values.yaml, update the repository value to "ghcr.io/stacksimplify/kubenginxhelm"
7. In deployment.yaml, remove autoscaling and serviceaccount references
8. In service.yaml, add nodeport argument with action to bring the port 31239 from values.yaml
9. In Chart.yaml, just change appversion and version to 1.0.0. This will anyway override when we create charts using starter charts but just want to compare and test it. 
10. In Chart.yaml, update the dependencies section. This will anyway override when we create charts using starter charts but just want to compare and test it. 
dependencies:
- name: mychart4
  version: "0.1.0"
  repository: "https://stacksimplify.github.io/helm-charts/"
11. Sub Charts: Download and untar a Helm Chart to "charts" directory. We are going to observe what happens to "charts" directory when we create a chart from starter chart
helm pull https://stacksimplify.github.io/helm-charts/mychart4-0.1.0.tgz --untar
12. Update NOTES.txt: remove if statement for Ingress
```

## Step-04: Test the Chart before converting it completely to Starter Chart
```t
# Change Directory
cd mystarterchart

# Helm Lint
helm lint 
URL: https://helm.sh/docs/helm/helm_lint/
1. examine a chart for possible issues
2. This command takes a path to a chart and runs a series of tests to verify that the chart is well-formed.
3. If the linter encounters things that will cause the chart to fail installation, it will emit [ERROR] messages. 
4. If it encounters issues that break with convention or recommendation, it will emit [WARNING] messages.

# Install Helm Release
helm install myapp1 . --rollback-on-failure

# List Pods and Services
kubectl get pods
kubectl get svc

# Access Application
Parent Chart: http://localhost:31239
mychart4 chart: http://localhost:<port-from-get-svc-output>

# Uninstall Helm Release
helm uninstall myapp1
```

## Step-05: Replace "mystarterchart" with `<CHARTNAME>` in all files
**Important Note:**  All occurrences of `<CHARTNAME>` will be replaced with the specified chart name so that starter charts can be used as templates.
1. _helpers.tpl
2. deployment.yaml
3. service.yaml
4. NOTES.txt
5. Chart.yaml
6. values.yaml (Here just in comment)


## Step-06: Copy mystarterchart to HELM_DATA_HOME/starters
```t
# Helm env command
helm env

# Helm env HELM_DATA_HOME
helm env HELM_DATA_HOME
HELM_DATA_HOME="/Users/kalyan/Library/helm"

# Create folder helm and helm/starters
cd /Users/kalyan/Library/
mkdir helm
cd helm
mkdir starters

# COPY mystarterchart folder 
cp -r mystarterchart /Users/kalyan/Library/helm/starters/
```

## Step-07: Create new chart using Starter Chart
- [Docker Image: kubenginxhelm](https://github.com/users/stacksimplify/packages/container/package/kubenginxhelm)
```t
# Change Directory
cd MYCHARTS

# Helm Create using starter chart
helm create mychart9 --starter=mystarterchart

# Review mychart9 files
1. Chart.yaml
- It should be regenerated and versions should be overided for both version and appversion to 0.1.0
- Update the appVersion to "0.3.0" with quotes(it should be string in quotes) 
- Our Docker Image version is also "0.3.0" which matches our Chart appVersion so we are good. 
- https://github.com/users/stacksimplify/packages/container/package/kubenginxhelm
2. deployment.yaml - Review it
3. service.yaml - Review it
4. values.yaml - Review it
5. NOTES.txt - Review it
6. "charts" directory: We should see "mychart4" should be present as packaged file "mychart4-0.1.0.tgz" even though in our starter chart we have it as UNZIPPED
```

## Step-08: Create Helm Release from new chart created using starter chart
```t
# Change Directory
cd MYCHARTS/mychart9

# Helm Lint
helm lint 

# Install Helm Release
helm install myapp901 .

# List Pods and Services
kubectl get pods
kubectl get svc

# Access Application
Parent Chart: http://localhost:31239
mychart4 chart: http://localhost:<port-from-get-svc-output>

# Uninstall Helm Release
helm uninstall myapp901
```

# Helm Plugins

## Step-01: Introduction
- Install Helm Plugins
- [Helm Starter Plugin](https://github.com/salesforce/helm-starter.git)
- [Helm Dashboard Plugin](https://github.com/komodorio/helm-dashboard.git)

## Step-02: Install Helm Plugin
- [Helm Starter Plugin](https://github.com/salesforce/helm-starter)
- [Review Helm Starter Plugin plugin.yaml](https://github.com/salesforce/helm-starter/blob/master/plugin.yaml)
```t
# List Helm Plugins
helm plugin list

# Install Helm Plugins
helm plugin install https://github.com/salesforce/helm-starter.git

# List Helm Plugins
helm plugin list

# Helm env
helm env 
Observation:
1. Find the value for HELM_PLUGINS
HELM_PLUGINS="/Users/kalyan/Library/helm/plugins"

# Verify in Helm plugins directory
cd /Users/kalyan/Library/helm/plugins
ls
```

## Step-03: Play with Helm Starter Plugin
```t
# List Helm Starters
helm plugin list
helm <PLUGIN-NAME> <PLUGIN-SUB-COMMAND-AS-PER-PLUGIN>
helm starter list

# Fetch Helm Starter
helm starter fetch https://github.com/salesforce/helm-starter-istio.git

# List Helm Starters
helm starter list
```

## Step-04: Play with Helm Plugin Commands
```t
# Update Helm Plugin
helm plugin list
helm plugin update PLUGIN-NAME
helm plugin update starter

# Uninstall Helm Plugin
helm plugin list
helm plugin uninstall PLUGIN-NAME
helm plugin uninstall starter
helm plugin list
```

## Step-05: Install Couple of Releases
```t
# Helm Rep Add
helm repo list
helm repo add stacksimplify https://stacksimplify.github.io/helm-charts/
helm repo list

# Helm Install dev101
helm install dev101 stacksimplify/mychart1 --rollback-on-failure
helm upgrade dev101 stacksimplify/mychart1 --rollback-on-failure --set replicaCount=2
helm upgrade dev101 stacksimplify/mychart1 --rollback-on-failure --set replicaCount=3

# Helm Install dev102
helm install dev102 stacksimplify/mychart2 --rollback-on-failure

# List Helm Releases
helm list
```

## Step-06: (Optional) Lets install Helm Dashboard Plugin
- [Helm Dashboard Plugin Git Repo](https://github.com/komodorio/helm-dashboard)
- [Helm Dashboard Plugin from Artifacthub](https://artifacthub.io/packages/helm-plugin/helm-dashboard/dashboard)
- [Review Helm Dashboard Plugin plugin.yaml](https://github.com/komodorio/helm-dashboard/blob/main/plugin.yaml)

```t
# List Helm Plugins
helm plugin list

# Install Helm Plugin
helm plugin install https://github.com/komodorio/helm-dashboard.git

# Start Helm Plugin: dashboard
helm dashboard

# Review Dashboard Concepts
1. Clusters
2. Installed Charts
    - Release: dev101 
        - Resources
        - Manifests
        - Values
        - Notes
    - Revision: 1, 2, 3 
    - Revision Differences
3. Repository
4. Logout 
```

## Step-07: Uninstall Releases
```t
# Helm Uninstall
helm uninstall dev101
helm uninstall dev102
```

# Build Helm Plugin

## Step-01: Introduction
- [Building Helm Plugins](https://helm.sh/docs/topics/plugins/#building-plugins)
- We will build 3 simple plugins and test

## Step-02: Create myplugin1 with env command -  Install and Verify
```t
# myplugin1
name: "myplugin1"
version: "0.1.0"
usage: "Printss Helm Environment Variables"
description: |-
  Prints Helm Environment Variables
command: "env"

# List Helm Plugins
helm plugin list

# Install Helm Plugin
helm plugin install myplugin1/

# List Helm Plugins
helm plugin list

# Run Helm Plugin
helm <PLUGIN-NAME>
helm myplugin1

# Observation
Prints Helm environment variables
```

## Step-03: Create myplugin2 with platformCommand -  Install and Verify
```t
# myplugin2
name: "myplugin2"
version: "0.1.0"
usage: "helm myplugin2"
description: "Print Helm plugin directory"
command: echo my helm plugin directory is $HELM_PLUGINS default command
platformCommand:
  - os: linux
    arch: i386
    command: "echo my helm plugin directory is $HELM_PLUGINS os is linux i386"
  - os: linux
    arch: amd64
    command: "echo my helm plugin directory is $HELM_PLUGINS os is linux amd64"
  - os: windows
    arch: amd64
    command: "echo my helm plugin directory is $HELM_PLUGINS os is windows amd64"

# List Helm Plugins
helm plugin list

# Install Helm Plugin
helm plugin install myplugin2/

# List Helm Plugins
helm plugin list

# Run Helm Plugin
helm <PLUGIN-NAME>
helm myplugin2

# Observation
Should execute the command from Default command section because we are running this on MacOS desktop which is not present in "platformCommand"
```
## Step-04: Create myplugin3 with shell script - Install and Verify
```t
# myplugin3
name: "myplugin3"
version: "0.1.0"
usage: "helm myplugin3"
description: "Print Helm plugin directory using script app.sh"
command: "$HELM_PLUGIN_DIR/app.sh"

# app.sh
#!/bin/sh
echo "my helm plugin directory is $HELM_PLUGINS from SHELL SCRIPT"

# List Helm Plugins
helm plugin list

# Install Helm Plugin
helm plugin install myplugin3/

# List Helm Plugins
helm plugin list

# Run Helm Plugin
helm <PLUGIN-NAME>
helm myplugin3

# Observation
We will see "app.sh" executed successfully
```

## Step-05: Uninstall Plugins
```t
# Uninstall Helm Plugins
helm plugin uninstall <PLUGIN-NAME>
helm plugin uninstall myplugin1
helm plugin uninstall myplugin2
helm plugin uninstall myplugin3
```


# Helm Hooks

## Step-01: Introduction
- Understand Helm Hooks

## Step-02: Create a simple Chart from Starter Chart 
- **Important Note:** This step is optional for you because you will have all the Chart files and folders ready for you to implement hooksdemo1 in this respective section
```t
# Create Helm Chart from starter chart
helm create hooksdemo1 --starter=mystarterchart
```

## Step-03: Create/Review pre-install Hook
- **File Location:** templates/preinstall-hookpod.yaml
```yaml
apiVersion: v1
kind: Pod
metadata: 
  name: myhook-preinstall
  annotations:
    "helm.sh/hook": "pre-install"
spec:
  restartPolicy: Never
  containers:
    - name: myhook-preinstall-container
      image: busybox
      imagePullPolicy: IfNotPresent
      command:  ['sh', '-c', 'echo Pre-install hook Pod is running && sleep 15']      
```


## Step-04: Create/Review pre-upgrade hook
- **File Location:** templates/preupgrade-hookpod.yaml
```yaml
apiVersion: v1
kind: Pod
metadata: 
  name: myhook-preupgrade
  annotations:
    "helm.sh/hook": "pre-upgrade"
spec:
  restartPolicy: Never
  containers:
    - name: myhook-preupgrade-container
      image: busybox
      imagePullPolicy: IfNotPresent
      command:  ['sh', '-c', 'echo preupgrade hook Pod is running && sleep 15']       
```

## Step-05: Create/Review post-delete hook
- **File Location:** templates/postdelete-hookpod.yaml
```yaml
apiVersion: v1
kind: Pod
metadata: 
  name: myhook-postdelete
  annotations:
    "helm.sh/hook": "post-delete"
spec:
  restartPolicy: Never
  containers:
    - name: myhook-postdelete-container
      image: busybox
      imagePullPolicy: IfNotPresent
      command:  ['sh', '-c', 'echo post-delete hook Pod is running && sleep 15']
```

## Step-06: Test Helm Hook: pre-install
```t
# Change Directory (In Helm Chart Folder)
cd hooksdemo1

# Install Helm Release
helm install myapp101 . --rollback-on-failure

# List Helm Release
helm list

# List Kubernetes Pods
kubectl get pods
Observation:
1. We should see "myhook-preinstall" pod which should be completed status

# Describe Pod
kubectl describe pod myhook-preinstall

# Verify Pod Start and Finish Times
kubectl get pods
kubectl describe pod myhook-preinstall | grep -E 'Anno|Started:|Finished:'
kubectl describe pod myapp101-hooksdemo1-65b7c4d5b9-2rqfx | grep -E 'Anno|Started:|Finished:'

# Access Application
kubectl get svc
http://localhost:31239
Observation: We should see V1 version of application
```

## Step-07: Hooks and the Release Lifecycle
1. Lets say for `helm install` lifecycle we have defined two hooks `pre-install` and `post-install`, lets understand what happens
2. Discuss by going to documentation [Hooks and the Release Lifecycle](https://helm.sh/docs/topics/charts_hooks/#hooks-and-the-release-lifecycle)

## Step-08: Test Helm Hook: pre-upgrade
```t
# Change Directory (In Helm Chart Folder)
cd hooksdemo1

# Upgrade Helm Release
helm list
helm upgrade myapp101 . --set image.tag=0.2.0

# List Kubernetes Pods
kubectl get pods
Observation:
1. We should see "myhook-preupgrade" pod which should be completed status

# Describe Pod
kubectl describe pod myhook-preupgrade

# Verify Pod Start and Finish Times
kubectl get pods
kubectl describe pod myhook-preupgrade | grep -E 'Anno|Started:|Finished:'
kubectl describe pod myapp101-hooksdemo1-7b997b4556-t6s75 | grep -E 'Anno|Started:|Finished:'

# Access Application
kubectl get svc
http://localhost:31239
Observation: We should see V2 version of Application
```

## Step-09: Test Helm Hook: post-delete
```t
# Change Directory (In Helm Chart Folder)
cd hooksdemo1

# Uninstall/Delete Helm Release
helm list
helm uninstall myapp101 

# List Kubernetes Pods
kubectl get pods
Observation:
1. We should see "myhook-postdelete" pod which should be completed status
2. We should see all the 3 hook pods present even after deleting/uninstalling the release
```

## Step-10: Hook resources are not managed with corresponding releases
1. The resources that a hook creates are currently not tracked or managed as part of the release. 
2. Once Helm verifies that the hook has reached its ready state, it will leave the hook resource alone.
3. In short, `helm uninstall` will not delete hook resources. 

