node {
  stage('Checkout') {
    checkout scm
  }

  withCredentials([
      usernamePassword(credentialsId: 'docker-credentials',
                       usernameVariable: 'USERNAME',
                       passwordVariable: 'PASSWORD')]) {
    stage('Build') {
      sh 'docker image build -t ${USERNAME}/demo-api:latest .'
    }
  }

  withCredentials([
      usernamePassword(credentialsId: 'docker-credentials',
                       usernameVariable: 'USERNAME',
                       passwordVariable: 'PASSWORD')]) {
    stage('Push') {
      sh 'docker login -p "${PASSWORD}" -u "${USERNAME}'
      sh 'docker image push ${USERNAME}/demo-api:latest'
    }
  }

  stage('Deploy') {
    // placeholder
  }
}
