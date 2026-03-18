resource "google_service_account" "cloudbuild_sa" {
    account_id   = "cloudbuild-sa"
    display_name = "Cloud Build Service Account"
}

resource "google_project_iam_member" "cloudbuild_sa_roles" {
    for_each = toset([
        "roles/run.admin",
        "roles/cloudbuild.builds.builder",
        "roles/artifactregistry.writer",
        "roles/clouddeploy.operator",
        "roles/iam.serviceAccountUser"
    ])

    project = var.project_id_gcp
    role    = each.value
    member  = "serviceAccount:${google_service_account.cloudbuild_sa.email}"
}