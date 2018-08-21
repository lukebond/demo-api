node {
  stage('Checkout') {
    checkout scm
  }

  stage('Build') {
    withCredentials([
        usernamePassword(credentialsId: 'docker-credentials',
                         usernameVariable: 'USERNAME',
                         passwordVariable: 'PASSWORD'),
        file(credentialsId: 'intoto-build_key',
             variable: 'INTOTO_BUILD_KEY'),
        file(credentialsId: 'intoto-root_key',
             variable: 'INTOTO_ROOT_KEY'),
        file(credentialsId: 'intoto-root.layout',
             variable: 'INTOTO_ROOT_LAYOUT')]) {
      sh '''#!/bin/bash -euo pipefail
        echo 1111111
        set -e
        echo 2222222
        set -u
        echo 3333333
        set -o pipefail
        echo 4444444
        exec 5>&1
        OUTPUT=$(docker image build -f Dockerfile-in-toto . | tee >(cat - >&5))
        IMAGE_ID=$(echo $OUTPUT | grep -B1 'FROM gliderlabs/alpine:3.6 as verify' | head -1 | awk '{print $2}')
        docker image tag ${IMAGE_ID} ${USERNAME}/demo-api:latest
      '''
    }
  }

  stage('Scan') {
    withCredentials([
        string(credentialsId: 'microscanner-token',
               variable: 'MICROSCANNER_TOKEN'),
        usernamePassword(credentialsId: 'docker-credentials',
                         usernameVariable: 'USERNAME',
                         passwordVariable: 'PASSWORD')]) {
      sh 'wget -q https://github.com/lukebond/microscanner-wrapper/raw/master/scan.sh -O /usr/local/bin/scan.sh && chmod +x /usr/local/bin/scan.sh'
      sh 'MICROSCANNER_OPTIONS=--continue-on-failure /usr/local/bin/scan.sh ${USERNAME}/demo-api:latest'
    }
  }

  stage('Sign') {
    withCredentials([
        usernamePassword(credentialsId: 'docker-credentials',
                         usernameVariable: 'USERNAME',
                         passwordVariable: 'PASSWORD')]) {
      sh '''
				GRAFEAS_HOST=10.10.5.147
				SIGNATURE_FILENAME=signature-${BUILD_NUMBER}.gpg
				GPG_EMAIL=luke@control-plane.io
				DIGEST=$(docker image inspect ${USERNAME}/demo-api:latest | jq -r .[0].Id)
				echo "${DIGEST}" | gpg2 --no-tty -u ${GPG_EMAIL} --armor --sign --output=${SIGNATURE_FILENAME}
				RESOURCE_URL=https://docker.io/${USERNAME}/demo-api@${DIGEST}
				GPG_SIGNATURE=$(cat ${SIGNATURE_FILENAME} | base64 -w 0)
				rm ${SIGNATURE_FILENAME}
				GPG_KEY_ID=$(gpg --no-tty --with-colons --with-fingerprint --force-v4-certs --list-keys ${GPG_EMAIL} | grep '^fpr' | awk -F: '{print $10}')
				cat > image-signing-occurence.json <<-EOF
				{
				  "resourceUrl": "${RESOURCE_URL}",
				  "noteName": "projects/image-signing/notes/production",
				  "attestation": {
				    "pgpSignedAttestation": {
				       "signature": "${GPG_SIGNATURE}",
				       "contentType": "application/text",
				       "pgpKeyId": "${GPG_KEY_ID}"
				    }
				  }
				}
				EOF
				curl -i -X POST \
				  "http://${GRAFEAS_HOST}:8081/v1alpha1/projects/image-signing/occurrences" \
				  -d @image-signing-occurence.json
      '''
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

  stage('Deploy') {
    withCredentials([
        file(credentialsId: 'kube-config',
             variable: 'KUBECONFIG')]) {
      //sh 'gpg2 --output - --verify signature.gpg'
      sh 'kubectl apply -f deployment.yaml'
    }
  }
}
