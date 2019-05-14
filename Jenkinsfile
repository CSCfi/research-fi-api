// This file is part of the research.fi API service
//
// Copyright 2019 Ministry of Education and Culture, Finland
//
// :author: CSC - IT Center for Science Ltd., Espoo Finland servicedesk@csc.fi
// :license: MIT
node {
  /*
   * Get source files from Git repository.
   */
  stage('Get source files from Git') {
    checkout scm
  }

  // Artifactory server
  def artifactory_server = "${env.ARTIFACTORY_SERVER}"
  // Docker registry in the Artifactory
  def registry = "${env.DOCKER_REGISTRY}"
  // Dockerfile name in the Git repository
  def dockerfile = "django/Dockerfile"
  // Docker image name
  def imagename = "researchfi-api-django"
  // Git branch name. Converted to lowercase letters to prevent problems when creating Docker image.
  def branchname = "${env.BRANCH_NAME}".toLowerCase()
  // Git commit hash to be used as a tag for the Docker image. Get the hash using shell script.
  def git_commit_hash = sh(returnStdout: true, script: "git log -n 1 --pretty=format:'%h'").trim()
  // Docker image tags 
  def tag_githash = "${registry}/${imagename}/${branchname}:${git_commit_hash}"
  def tag_latest = "${registry}/${imagename}/${branchname}:latest"

  /*
   * Print environment variables for Jenkins pipeline debugging purposes.
   */
  stage('Print environment variables') {
    echo sh(returnStdout: true, script: 'env')
  }

 /*
   * Build and tag Docker image
   */
  stage('Build and tag Docker image') {
    sh "docker build -f ${dockerfile} -t ${tag_githash} -t ${tag_latest} django/"
  }

  /*
   * Push Docker image to registry only if Git branch is 'master' or 'devel'
   */
  //if ("${branchname}" == "master" || "${branchname}" == "devel") {
    stage('Push Docker image') {
      withDockerRegistry(url: "https://${registry}", credentialsId: 'artifactory-credentials') {
        sh "docker push ${tag_githash}"
        sh "docker push ${tag_latest}"
      }
    }
  //}

  /*
   * Cleanup. Delete unused Docker items: containers, images etc.
   * NOTE! Uses 'system prune' commang to blindly remove any dangling items.
   * This can be used as long as the project has dedicated Jenkins instance.
   */
  stage('Cleanup') {
    sh 'docker system prune -f'
  }
}