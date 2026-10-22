
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out QRVerify source code'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                sh 'python3 --version'
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Test Application') {
            steps {
                echo 'Running QRVerify validation'
                sh '.venv/bin/python -m py_compile app.py'
                sh '.venv/bin/python -c "import app; print(1)"'
            }
        }
        
       
        stage('Build Docker Image') {
            steps {
                echo 'Building QRVerify Docker image'
                sh 'docker build -t qrverify:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds-system',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag qrverify:latest "$DOCKER_USER/qrverify:latest"
                        docker push "$DOCKER_USER/qrverify:latest"
                        docker logout
                    '''
                }
            }
        }


    }

    post {
        success {
            echo 'QRVerify pipeline completed successfully!'
        }
        failure {
            echo 'QRVerify pipeline failed. Check the stage logs.'
        }
    }
}
