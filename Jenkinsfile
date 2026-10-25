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
    }
}
