node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool 'SonarQube';
    withSonarQubeEnv(installationName: 'SonarQube') {
      sh "./bin/sonar-scanner"
    }
  }
}