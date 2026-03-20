module "artifact-registry" {
    source = "../../modules/artifact-registry"
    project_name = var.project_name
    environment = var.environment
    region = var.region
}

module "app_service" {
    source = "../../modules/cloud-run-service"
    project_name = var.project_name
    environment = var.environment
    region = var.region
    container_port = var.container_port
    ingress_type = "internal-and-cloud-load-balancing"
    security_type = "allUsers"
}

module "neg_app_service" {
    source = "../../modules/neg"
    project_name = var.project_name
    environment = var.environment
    region = var.region
    service_name = module.app_service.service_name
    endpoint_type = "SERVERLESS"
}

module "clouddeploy_target_cloud_run" {
    source = "../../modules/cloud_deploy_targets"
    project_name = var.project_name
    environment = var.environment
    region = var.region
    project_id_gcp = var.project_id_gcp
    canary_environment = "cloudrun"
}

module "clouddeploy_pipieline" {
    source = "../../modules/cloud_deploy_delivery_pipeline"
    project_name = var.project_name
    environment = var.environment
    region = var.region
    cloud_run_target = module.clouddeploy_target_cloud_run.target_name
}

module "cloudbuild_sa" {
    source = "../../modules/service-account-cloud-build"
    project_name = var.project_name
    environment = var.environment
    region = var.region
    project_id_gcp = var.project_id_gcp
}

module "cloudbuild_repository" {
    source = "../../modules/cloud_build_repository"
    project_name = var.project_name
    environment = var.environment
    region = var.region
    gh_repo = var.gh_repo
    gh_conn_name = var.gh_conn_name
    owner = var.owner
}

module "cloudbuild_trigger" {
    source = "../../modules/cloud_build_trigger"
    project_name = var.project_name
    environment = var.environment
    region = var.region
    container_port = var.container_port
    gh_branch = var.gh_branch
    artifact_repo = module.artifact-registry.repo_name
    repository_id = module.cloudbuild_repository.repository_id
    sa_id = module.cloudbuild_sa.sa_id
    service_name = module.app_service.service_name
    pipeline_name = module.clouddeploy_pipieline.pipeline_name
}