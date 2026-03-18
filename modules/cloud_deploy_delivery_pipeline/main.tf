resource "google_clouddeploy_delivery_pipeline" "pipeline" {
    name     = "${var.environment}-${var.project_name}-pipeline"
    location = var.region

    serial_pipeline {
        stages {
        target_id = var.green_target
        }

        stages {
        target_id = var.blue_target

        strategy {
            canary {
            runtime_config {
                cloud_run {
                automatic_traffic_control = true
                }
            }

            canary_deployment {
                percentages = [10, 30, 60]
                verify      = true
            }
            }
        }
        }
    }
}