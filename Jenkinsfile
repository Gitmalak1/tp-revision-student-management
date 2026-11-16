pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Linux : sh | Windows : remplacer sh par bat
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install flask selenium'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m unittest test_student_manager -v'
            }
        }
    }

    post {
        success { echo 'Pipeline réussi' }
        failure { echo 'Pipeline échoué : un test a échoué' }
    }
}
