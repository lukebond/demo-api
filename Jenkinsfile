node {
  stage('Checkout') {
    checkout scm
  }

  stage('Build') {
    sh 'docker image build -t lukebond/demo-api:latest .'
  }

  stage('Deploy') {
    // placeholder
  }
}
