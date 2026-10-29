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
                    ./venv/bin/pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
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
                    ./venv/bin/python -m pytest tests/api/ -v --junitxml=reports/api-junit.xml
                '''
            }
        }

        stage('UI 测试') {
            steps {
                sh '''
                    # 清理可能残留的旧容器，避免名字冲突
                    docker rm -f selenium-firefox || true

                    # 启动 Selenium 容器，--add-host 让容器内能通过 host.docker.internal 访问宿主机
                    docker run -d --name selenium-firefox -p 4444:4444 --shm-size="2g" \
                        --add-host=host.docker.internal:host-gateway \
                        selenium/standalone-firefox:latest

                    # 等待 Selenium 就绪，最多 30 秒
                    for i in $(seq 1 30); do
                        if curl -s http://127.0.0.1:4444/status | grep -q '"ready": true'; then
                            break
                        fi
                        sleep 1
                    done

                    # 清除代理变量，避免 pytest 连接本地 Selenium 时误走代理
                    unset http_proxy https_proxy all_proxy
                    unset HTTP_PROXY HTTPS_PROXY ALL_PROXY

                    mkdir -p reports
                    ./venv/bin/python -m pytest tests/ui/ -v --junitxml=reports/ui-junit.xml
                '''
            }
            post {
                always {
                    sh 'docker rm -f selenium-firefox || true'
                }
            }
        }
    }

    post {
        always {
            script {
                if (fileExists('reports/api-junit.xml')) {
                    junit 'reports/api-junit.xml'
                }
                if (fileExists('reports/ui-junit.xml')) {
                    junit 'reports/ui-junit.xml'
                }
            }
        }
    }
}