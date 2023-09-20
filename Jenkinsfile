pipeline {
  agent any

  stages {
    stage('1. LẤY MÃ NGUỒN TỪ GIT REPOSITORY') {
      steps {
        script {
          checkout scm
        }
      }
    }
    stage('2. QUÉT MÃ NGUỒN VỚI SONARQUBE SCANNER') {
      steps {
        script {
          def scannerHome = tool 'SonarScanner';
          withSonarQubeEnv() {
            sh "${scannerHome}/bin/sonar-scanner"
          }
        }
      }
    }
    stage("3. PHẢN HỒI KẾT QUẢ QUÉT MÃ NGUỒN") {
      steps {
        script {
          timeout(time: 1, unit: 'HOURS') { // Just in case something goes wrong, pipeline will be killed after a timeout
            def qg = waitForQualityGate(); // Reuse taskId previously collected by withSonarQubeEnv
              if (qg.status != 'OK') {
                error "Kết quả: Mã nguồn không đạt yêu cầu ${qg.status}"
              }
          }
        }
      }
    }
    stage("4. XÂY DỰNG IMAGE VÀ CHUẨN BỊ MÔI TRƯỜNG ROLLBACK") {
      steps {
        script {
          def imageName = 'nssa/servicedeskform1';
          def testContainerName = 'servicedeskform1_test';
          def testTag = 'test';
          def testPort = 51814;
          // Check if the Docker container exists
          def containerExists = sh(script: "docker ps -a --format '{{.Names}}' | grep -q '^${testContainerName}\$'", returnStatus: true)
          // Check if the Docker image exists
          def imageExists = sh(script: "docker images --format '{{.Repository}}:{{.Tag}}' | grep -q '^${imageName}:${testTag}\$'", returnStatus: true)
          // Remove the Docker container if it exists
          if (containerExists == 0) {
              sh "docker stop ${testContainerName}"
              sh "docker rm ${testContainerName}"
          } else {
              echo "Docker container '${testContainerName}' does not exist."
          }

          // Remove the Docker image if it exists
          if (imageExists == 0) {
              sh "docker image rm ${imageName}:${testTag} -f";
              sh "docker build --file ./ServiceDeskForm/Dockerfile --tag ${imageName}:${testTag} --build-arg port=${testPort} .";
          } else {
              echo "Docker image '${imageName}' does not exist."
              sh "docker build --file ./ServiceDeskForm/Dockerfile --tag ${imageName}:${testTag} --build-arg port=${testPort} .";
          }
        }
      }
    }
    stage("5. TRIỂN KHAI MÔI TRƯỜNG KIỂM THỬ") {
      steps {
        script {
          def testContainerName = 'servicedeskform1_test';
          def testPort = 51814;
          def imageName = 'nssa/servicedeskform1';
          def testTag = 'test';
          sh "docker run -d --name ${testContainerName} -p ${testPort}:51813 ${imageName}:${testTag}";
        }
      }
    }
    stage("6. CHẠY KỊCH BẢN KIỂM THỬ") {
      steps {
        script {
          def websiteUrl = "http://docker01.dc.vn:51814"
          def maxRetries = 3
          def retryCount = 0
          timeout(time: 1, unit: 'MINUTES') {
            waitUntil {
              try {         
                sh "curl -s --head  --request GET $websiteUrl | grep '200 OK'"
                return true
              } catch (Exception e) {
                return false
              }
            }
          }
        }
      }
    }
    stage("7. TRIỂN KHAI MÔI TRƯỜNG CHÍNH THỨC") {
      steps {
        script {
          def imageName = 'nssa/servicedeskform1';
          def prodContainerName = 'servicedeskform1_test';
          def latestTag = 'lts';
          def prodPort = 51813;
          def rollBacktag = 'rollback';
          // Check if production container exist
          def containerExists = sh(script: "docker ps -a --format '{{.Names}}' | grep -q '^${prodContainerName}\$'", returnStatus: true)
          if (containerExists == 0) {
              sh "docker stop ${prodContainerName}"
              sh "docker rm ${prodContainerName}"
          } else {
              echo "Docker container '${prodContainerName}' does not exist."
          }

          // Check if production image exist
          def lst_imageExists = sh(script: "docker images --format '{{.Repository}}:{{.Tag}}' | grep -q '^${imageName}:${latestTag}\$'", returnStatus: true)
          def rollback_imageExists = sh(script: "docker images --format '{{.Repository}}:{{.Tag}}' | grep -q '^${imageName}:${rollBacktag}\$'", returnStatus: true)
          if (lst_imageExists == 0) {
              if (rollback_imageExists == 0) {
                sh "docker image rm ${imageName}:${rollBacktag} -f";
                sh "docker image tag ${imageName}:${latestTag} ${imageName}:${rollBacktag}";
                sh "docker image rm ${imageName}:${latestTag}";
                sh "docker build --file ./ServiceDeskForm/Dockerfile --tag ${imageName}:${latestTag} --build-arg port=${prodPort} .";
              } else {
                echo "Docker image '${rollback_imageExists}' does not exist."
                sh "docker image tag ${imageName}:${latestTag} ${imageName}:${rollBacktag}";
                sh "docker build --file ./ServiceDeskForm/Dockerfile --tag ${imageName}:${latestTag} --build-arg port=${prodPort} .";
              }
          } else {
            echo "Docker image '${lst_imageExists}' does not exist."
            sh "docker build --file ./ServiceDeskForm/Dockerfile --tag ${imageName}:${latestTag} --build-arg port=${prodPort} .";
          }
          sh "docker run -d --name ${prodContainerName} -p ${prodPort}:51813 ${imageName}:${latestTag}";
        }
      }
    }
    stage("8. Kiểm tra hoạt động trên môi trường chính thức")
      steps {
        script {
          def websiteUrl = "http://docker01.dc.vn:51813"
          def maxRetries = 3
          def retryCount = 0
          timeout(time: 1, unit: 'MINUTES') {
            waitUntil {
              try {         
                sh "curl -s --head  --request GET $websiteUrl | grep '200 OK'"
                return true
              } catch (Exception e) {
                return false
              }
            }
          }
        }
      }
  }
}