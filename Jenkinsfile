import groovy.transform.Field

@Field
def metadataService = 'https://in-toto-webhook.in-toto.svc'
@Field
def namespace = 'cloudnativeglasgow'
@Field
def imageTag = 'demo-gods'

pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build') {
      steps {
        in_toto_wrap([
            'stepName': 'build',
            'credentialId': 'build_key',
            'transport': "${metadataService}/links/${namespace}/build"]) {
          echo 'Building..'
          sh "docker image build -t lukebond/demo-api:${imageTag} ."
        }
      }
    }
/*
    stage('Scan') {
      steps {
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
    }

    stage('Sign') {
      steps {
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
    }
*/

    stage('Push') {
      steps {
        withCredentials([
            usernamePassword(credentialsId: 'docker-credentials',
                             usernameVariable: 'USERNAME',
                             passwordVariable: 'PASSWORD')]) {
          sh "echo ${PASSWORD} | docker login --password-stdin -u ${USERNAME}"
          sh "docker image push ${USERNAME}/demo-api:${imageTag}"
        }
      }
    }

/*
    stage('Deploy') {
      steps {
        withCredentials([
            file(credentialsId: 'kube-config',
                 variable: 'KUBECONFIG')]) {
          //sh 'gpg2 --output - --verify signature.gpg'
          sh 'kubectl apply -f deployment.yaml'
        }
      }
    }
*/
  }
}
