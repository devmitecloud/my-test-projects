# `eks/helm/basechart` File Structure

This directory is a standard Helm application chart named `basechart`. It packages Kubernetes manifests as templates so the same chart can be reused with different values at deploy time.

## Top-level files

### `Chart.yaml`

This is the chart metadata file.

- Declares this chart as Helm API version `v2`.
- Sets the chart name to `basechart`.
- Marks the chart as `type: application`, which means it renders deployable Kubernetes resources.
- Defines the chart package version as `0.1.0`.
- Defines the default application version as `1.16.0`.

Helm uses this file for packaging, dependency handling, versioning, and release metadata.

### `values.yaml`

This is the default configuration input for the chart.

It provides the values consumed by the templates under `templates/`, including:

- `replicaCount` for deployment replica count when autoscaling is off.
- `image.repository`, `image.tag`, and `image.pullPolicy` for the container image.
- `imagePullSecrets` for private registry access.
- `nameOverride` and `fullnameOverride` for naming control.
- `serviceAccount.*` for whether to create a service account, its name, annotations, and token automount behavior.
- `podAnnotations`, `podLabels`, `podSecurityContext`, and `securityContext` for pod/container metadata and security settings.
- `service.type` and `service.port` for the Kubernetes Service.
- `ingress.*` to optionally create an Ingress resource.
- `httpRoute.*` to optionally create a Gateway API `HTTPRoute`.
- `resources`, `livenessProbe`, and `readinessProbe` for runtime configuration.
- `autoscaling.*` to optionally create an HPA.
- `volumes` and `volumeMounts` for extra storage configuration.
- `nodeSelector`, `tolerations`, and `affinity` for pod scheduling.

In Helm terms, this file is the main customization surface for anyone installing the chart.

### `.helmignore`

This file works like `.gitignore`, but for Helm chart packaging.

- Excludes files such as `.DS_Store`, VCS directories like `.git/`, editor folders like `.vscode/`, and temporary files like `*.swp`.
- Prevents unnecessary local files from being included when running `helm package`.

### `charts/`

This directory is where Helm dependencies or subcharts are stored.

- It is currently empty.
- If this chart depended on other charts, packaged dependencies would appear here, or Helm would populate it during dependency build/update.

## `templates/` files

Everything in `templates/` is rendered by Helm into Kubernetes manifests using the values from `values.yaml` and release metadata.

### `templates/_helpers.tpl`
In the template any file that begins with underscore is not ecpected to putput a kubernetes manifest file.
This file defines reusable Helm template helper functions.

It contains helpers for:

- `basechart.name`: returns the chart name or `nameOverride`.
- `basechart.fullname`: builds the full release resource name, respecting `fullnameOverride` and Helm release naming.
- `basechart.chart`: creates the `helm.sh/chart` label value.
- `basechart.labels`: standard common labels used across resources.
- `basechart.selectorLabels`: the selector labels shared by Deployment and Service.
- `basechart.serviceAccountName`: resolves the service account name depending on whether the chart creates one.

This file does not create Kubernetes resources directly. It exists to keep naming and labels consistent across templates.

### `templates/deployment.yaml`

This template creates the main `Deployment` for the application.

It does the following:

- Names the Deployment using `basechart.fullname`.
- Applies common chart labels.
- Sets `.spec.replicas` from `replicaCount` only when autoscaling is disabled.
- Uses selector labels from `_helpers.tpl` so the Service can target the same pods.
- Adds optional pod annotations and extra pod labels.
- Sets optional `imagePullSecrets`.
- Sets `serviceAccountName` using the helper.
- Applies optional pod security context and container security context.
- Runs a single container using `image.repository` and `image.tag` or falls back to `.Chart.AppVersion`.
- Exposes one named container port `http` using `.Values.service.port`.
- Adds optional liveness and readiness probes.
- Adds optional resource requests/limits.
- Adds optional `volumeMounts`, `volumes`, `nodeSelector`, `affinity`, and `tolerations`.

This is the core workload template in the chart.

### `templates/service.yaml`

This template creates a Kubernetes `Service` in front of the Deployment.

- Uses the same full name as the Deployment.
- Uses the same selector labels so traffic goes to the chart's pods.
- Sets the service type from `service.type`.
- Exposes one port from `service.port`.
- Sends traffic to the container's named `http` port.

This is the stable internal endpoint that other traffic-entry resources point to.

### `templates/ingress.yaml`

This template creates an `Ingress`, but only if `ingress.enabled` is `true`.

It supports:

- Optional ingress annotations.
- Optional `ingressClassName`.
- Optional TLS configuration.
- Multiple hosts and paths from `ingress.hosts`.
- Routing each path to the chart's Service on `service.port`.

Use this when the cluster exposes HTTP traffic through a traditional Ingress controller such as NGINX or AWS ALB Ingress Controller, depending on cluster setup.

### `templates/httproute.yaml`

This template creates a Gateway API `HTTPRoute`, but only if `httpRoute.enabled` is `true`.

It supports:

- Optional annotations.
- `parentRefs` to attach the route to one or more Gateways/listeners.
- Optional `hostnames`.
- Configurable `rules` with `matches` and optional `filters`.
- A backend reference pointing to this chart's Service on `service.port`.

This is the newer Gateway API equivalent to using Ingress. It is only useful if the cluster has Gateway API CRDs and a compatible controller installed.

### `templates/hpa.yaml`

This template creates a `HorizontalPodAutoscaler`, but only if `autoscaling.enabled` is `true`.

It:

- Targets the Deployment created by this chart.
- Sets `minReplicas` and `maxReplicas` from `autoscaling` values.
- Optionally adds CPU utilization scaling if `targetCPUUtilizationPercentage` is set.
- Optionally adds memory utilization scaling if `targetMemoryUtilizationPercentage` is set.

Because the Deployment template skips `.spec.replicas` when autoscaling is enabled, the HPA becomes the source of truth for scaling.

### `templates/serviceaccount.yaml`

This template creates a Kubernetes `ServiceAccount`, but only if `serviceAccount.create` is `true`.

It:

- Uses the helper-generated name or `serviceAccount.name`.
- Applies standard labels.
- Adds optional annotations.
- Sets `automountServiceAccountToken` from `serviceAccount.automount`.

The Deployment then references this service account via `serviceAccountName`.

### `templates/NOTES.txt`

This is not a Kubernetes resource. It is a post-install/post-upgrade message shown by Helm after a release is installed.

It prints different usage instructions depending on how the app is exposed:

- `HTTPRoute` instructions if `httpRoute.enabled` is on.
- Ingress URLs if `ingress.enabled` is on.
- NodePort access instructions if the service type is `NodePort`.
- LoadBalancer access instructions if the service type is `LoadBalancer`.
- `kubectl port-forward` instructions if the service type is `ClusterIP`.

This improves operator usability by telling the installer how to reach the application after deployment.

### `templates/tests/test-connection.yaml`

This template defines a Helm test pod.

- Annotated with `helm.sh/hook: test`, so it runs when `helm test` is executed.
- Launches a small `busybox` container.
- Runs `wget` against `<service-name>:<service-port>` to verify the Service is reachable.
- Uses `restartPolicy: Never` because it is a one-off validation pod.

This is a lightweight connectivity smoke test for the deployed release.

## Overall chart behavior

At a high level, this chart deploys:

- A `Deployment` for the workload.
- A `Service` for stable access to the pods.
- Optionally a `ServiceAccount`.
- Optionally an `Ingress` or `HTTPRoute` for external HTTP exposure.
- Optionally an `HorizontalPodAutoscaler` for scaling.
- A Helm test pod for basic post-deploy connectivity checks.

This is essentially a standard Helm starter chart, with one notable extension: support for both classic `Ingress` and Gateway API `HTTPRoute` exposure models.
