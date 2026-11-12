pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['smoke', 'all'],
            description: '选择测试集：smoke 只跑冒烟，all 跑全量并允许打包'
        )
        booleanParam(
            name: 'RUN_UI_TESTS',
            defaultValue: false,
            description: '是否运行 UI 测试（手动勾选，自动触发时默认关闭）'
        )
    }

    triggers {
        pollSCM('H/5 * * * *')
    }

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

        stage('接口测试') {
            steps {
                script {
                    def markerArg = params.TEST_SUITE == 'all' ? '' : '-m smoke'
                    sh """
                        mkdir -p reports
                        ./venv/bin/python -m pytest tests/api/ -v ${markerArg} \
                            --junitxml=reports/api-junit.xml
                    """
                }
            }
        }

        stage('UI 测试') {
            when {
                expression { params.RUN_UI_TESTS == true }
            }
            steps {
                sh '''
                    docker rm -f selenium-firefox || true
                    docker run -d --name selenium-firefox -p 4444:4444 --shm-size="2g" \
                        --add-host=host.docker.internal:host-gateway \
                        selenium/standalone-firefox:latest
                    for i in $(seq 1 30); do
                        if curl -s http://127.0.0.1:4444/status | grep -q '"ready": true'; then
                            break
                        fi
                        sleep 1
                    done
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

	stage('UI 测试 (Playwright)') {
	    agent {
	        docker {
	            image 'mcr.microsoft.com/playwright/python:v1.64.1-noble'
	            args '-u root --ipc=host --network host'
	        }
	    }
	    steps {
	        sh '''
	            pip install -r requirements.txt
	            pytest tests/ui_playwright/ -v --junitxml=reports/ui-junit.xml \
		    --alluredir=reports/allure-results \
                    --clean-alluredir
	        '''
	    }
	}

        stage('构建镜像') {
            when {
                expression { params.TEST_SUITE == 'all' }
            }
            steps {
                sh '''
                    IMAGE_TAG=$(git rev-parse --short HEAD)
                    docker build -t hr-system:${IMAGE_TAG} .
                    docker tag hr-system:${IMAGE_TAG} hr-system:latest
                    echo "镜像已构建: hr-system:${IMAGE_TAG}"
                '''
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
                if (fileExists('reports/allure-results')){
                    allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]  
               }
            }
        }
    }
}
