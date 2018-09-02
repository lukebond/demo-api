node {
  stage('Checkout') {
    checkout scm
  }

  //stage('Verify') {
  //  withCredentials([
  //      file(credentialsId: 'keybase-envfile',
  //           usernameVariable: 'KEYBASE_ENV_FILE')]) {
  //    def scmUrl = scm.getUserRemoteConfigs()[0].getUrl()
  //    sh '''
  //      docker run -it --env-file=${KEYBASE_ENV_FILE} \
  //        -e KEYBASE_TRUSTED_USERS=lukebond \
  //        -e GIT_USER_EMAIL="luke.n.bond+bot@gmail.com" \
  //        -e GIT_REPO="${scmUrl}" \
  //        -e GIT_REVISIONS_TO_VERIFY=1 \
  //        controlplane/keybase:latest
  //    '''
  //  }
  //}

  stage('Build') {
    withCredentials([
        usernamePassword(credentialsId: 'docker-credentials',
                         usernameVariable: 'USERNAME',
                         passwordVariable: 'PASSWORD')]) {
      sh 'docker image build -t ${USERNAME}/demo-api:latest .'
    }
  }

  stage('Push') {
    withCredentials([
        usernamePassword(credentialsId: 'docker-credentials',
                         usernameVariable: 'USERNAME',
                         passwordVariable: 'PASSWORD')]) {
      sh 'docker login -p "${PASSWORD}" -u "${USERNAME}"'
      sh 'docker image push ${USERNAME}/demo-api:latest'
    }
  }

  stage('Kubetest') {
    sh """
      echo 'Running Kubetest...'

      wget https://github.com/garethr/kubetest/releases/download/0.1.1/kubetest-linux-amd64.tar.gz
      tar xf kubetest-linux-amd64.tar.gz

      if ./kubetest ./deployment.yaml; then
        exit 0;
      fi

      exit 1
    """
  }

  stage('Kubesec') {
    sh """
      echo 'Running Kubesec...'

      if curl --silent \
          --compressed \
          --connect-timeout 5 \
          -F file=@deployment.yaml \
          https://kubesec.io/ | jq --exit-status '.score > 10' >/dev/null; then
        exit 0;
      fi

      echo 'The application failed on kubesec score'
      exit 1
    """
  }

  stage('Deploy') {
    withCredentials([
        file(credentialsId: 'kube-config',
             variable: 'KUBECONFIG')]) {
      sh 'kubectl apply -f deployment.yaml'
    }
  }
}
