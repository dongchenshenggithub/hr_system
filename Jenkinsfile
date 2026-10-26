pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('安装依赖') {
            steps {
                sh '''
                    rm -rf venv
                    python3 -m venv venv
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('启动检查') {
            steps {
                sh '''
                    ./venv/bin/python -c "from app.main import app; print('app loaded:', app.title)"
                '''
            }
        }

        stage('接口测试') {
            steps {
                sh '''
                    mkdir -p reports
                    ./venv/bin/python -m pytest -v --junitxml=reports/junit.xml
                '''
            }
        }
    }

    post {
        always {
            script {
                if (fileExists('reports/junit.xml')) {
                    junit 'reports/junit.xml'
                }
            }
        }
    }
}
