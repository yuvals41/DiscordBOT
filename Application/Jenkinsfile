pipeline {
    agent {
        label 'docker'
    }
    options {
        timestamps()
        ansiColor('xterm')
        timeout(time: 5, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr:'100'))
    }
    environment {
        JOB_BUILD_CAUSE = "${currentBuild.getBuildCauses()[0].shortDescription}"
    }
    libraries {
        lib('pipeline-library')
    }
    stages {
        stage('init') {
          steps {
              script {
                    hello.hello()

                    def String yuval = hello.yuval_is_the_best("yuval")
                    echo "$yuval"
                }
            }
        }
    }
}
