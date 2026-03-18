resource "google_cloud_run_service" "app_service" {
    name = "${var.environment}-${var.project_name}-app-service"
    location = var.region

    template {
        spec {
            containers {
                image = "us-docker.pkg.dev/cloudrun/container/hello"
            }
        }
    }

    metadata {
        annotations = {
            "run.googleapis.com/ingress" = var.ingress_type
        }
    }
}

resource "google_cloud_run_service_iam_policy" "public_invoker" {
    location = google_cloud_run_service.app_service.location
    project  = google_cloud_run_service.app_service.project
    service  = google_cloud_run_service.app_service.name

    policy_data = data.google_iam_policy.permission.policy_data
}