import groovy.transform.Field

@Field
def metadataService = 'https://in-toto-webhook.in-toto.svc'
@Field
def namespace = 'lukebond'
@Field
def imageRepo = 'demo-api'
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
            'credentialId': 'jenkins_key',
            'transport': "${metadataService}/links/${namespace}/${imageRepo}/build.4c6d68dc.link"]) {
          echo 'Building..'
          sh "docker image build -t lukebond/demo-api:${imageTag} ."
        }
      }
    }

    stage('Scan') {
      steps {
        in_toto_wrap([
            'stepName': 'scan',
            'credentialId': 'jenkins_key',
            'transport': "${metadataService}/links/${namespace}/${imageRepo}/scan.4c6d68dc.link"]) {
          withCredentials([
              string(credentialsId: 'microscanner-token',
                     variable: 'MICROSCANNER_TOKEN')]) {
            sh 'wget -q https://github.com/lukebond/microscanner-wrapper/raw/master/scan.sh -O scan.sh && chmod +x scan.sh'
            sh 'wget -q https://github.com/lukebond/microscanner-wrapper/raw/master/grabjson.sh -O grabjson.sh && chmod +x grabjson.sh'
            sh "MICROSCANNER_OPTIONS=\"--continue-on-failure\" ./grabjson.sh lukebond/demo-api:${imageTag} > microscanner-report.json"
          }
        }
      }
    }
/*
    stage('Kubesec') {
      steps {
        in_toto_wrap([
            'stepName': 'kubesec',
            'credentialId': 'jenkins_key',
            'transport': "${metadataService}/links/${namespace}/${imageRepo}/kubesec.4c6d68dc.link"]) {
          sh '''
						curl --silent \
						  --compressed \
						  --connect-timeout 5 \
						  -F file=@pod.yaml \
						  https://kubesec.io/ > kubesec-report.json
          '''
        }
      }
    }
/*
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

    stage('Deploy') {
      steps {
        withCredentials([
            file(credentialsId: 'kube-config',
                 variable: 'KUBECONFIG')]) {
          sh 'kubectl apply -f pod.yaml'
        }
      }
    }
  }
}
