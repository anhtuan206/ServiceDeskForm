node {
  stage('1. LẤY MÃ NGUỒN TỪ GIT REPOSITORY') {
    checkout scm
  }
  stage('2. QUÉT MÃ NGUỒN VỚI SONARQUBE SCANNER') {
    def scannerHome = tool 'SonarScanner';
    withSonarQubeEnv() {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }
  stage("3. PHẢN HỒI KẾT QUẢ QUÉT MÃ NGUỒN") {
    timeout(time: 1, unit: 'HOURS') { // Just in case something goes wrong, pipeline will be killed after a timeout
      def qg = waitForQualityGate(); // Reuse taskId previously collected by withSonarQubeEnv
        if (qg.status != 'OK') {
          error "Kết quả: Mã nguồn không đạt yêu cầu ${qg.status}"
        }
    }
  }
  stage("4. XÂY DỰNG IMAGE VÀ CHUẨN BỊ MÔI TRƯỜNG ROLLBACK") {
    def imageName = 'nssa/servicedeskform1';
    def rollBacktag = 'rollback';
    def latestTag = 'lts';
    def testTag = 'test';
    def testPort = 51814;
    sh "docker stop ${testContainerName}";
    sh "docker rm ${testContainerName}";
    sh "docker image rm ${imageName}:${testTag}";
    sh "docker build --file ./ServiceDeskForm/Dockerfile --tag ${imageName}:${testTag} --build-arg port=${testPort} .";
  }
  stage("5. TRIỂN KHAI MÔI TRƯỜNG KIỂM THỬ") {
    def testContainerName = 'servicedeskform1_test';
    def testPort = 51814;
    def imageName = 'nssa/servicedeskform1';
    def testTag = 'test';
    sh "docker run -d --name ${testContainerName} -p ${testPort}:51813 ${imageName}:${testTag}";
  }
  stage("6. CHẠY KỊCH BẢN KIỂM THỬ") {
    sh "echo 'Kịch bản kiểm thử'";
  }
  stage("7. TRIỂN KHAI MÔI TRƯỜNG CHÍNH THỨC") {
    def imageName = 'nssa/servicedeskform1';
    def prodContainerName = 'servicedeskform1_test';
    def latestTag = 'lts';
    def prodPort = 51813;
    def rollBacktag = 'rollback';

    sh "docker image rm ${imageName}:${rollBacktag}";
    sh "docker image tag ${imageName}:${latestTag} ${imageName}:${rollBacktag}";
    sh "docker stop ${prodContainerName}";
    sh "docker rm ${prodContainerName}";
    sh "docker run -d --name ${prodContainerName} -p ${prodPort}:51813 ${imageName}:${latestTag}";

  }
}