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
		    reuseNode true
	        }
	    }
	    steps {
	        sh '''
	            pip install -r requirements.txt
	            # 启动 uvicorn，监听 0.0.0.0，让容器内浏览器能访问
        	    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
          	    UVICORN_PID=$!

           	    # 等待服务就绪，最多 15 秒
           	    for i in $(seq 1 15); do
              	     if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health | grep -q "200"; then
               	        break
              	     fi
              	     sleep 1
           	    done
	            pytest tests/ui_playwright/ -v --junitxml=reports/ui-junit.xml \
		    --alluredir=reports/allure-results \
                    --clean-alluredir \
                    --tracing retain-on-failure
           	    kill $UVICORN_PID || true
          	    chown -R 112:115 reports/allure-results
	        '''
            // 旧代码：stash 写在 steps 末尾，pytest 一旦失败就不会执行，
            // 导致 post always 里的 unstash 找不到 stash 而抛异常
            // stash includes: 'reports/allure-results/**', name: 'allure-results'
	    }
	    post {
	        always {
	            // allowEmpty: true 让 pytest 早期失败、结果目录为空时也能 stash 成功，
	            // 保证 unstash 永远不会因为 stash 不存在而抛异常
	            stash includes: 'reports/allure-results/**', name: 'allure-results', allowEmpty: true
	        }
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
                // 旧代码：三引号在 Groovy 里只是字符串字面量，if 判断从未生效，
                // 导致 unstash 和 allure 无条件执行；stash 不存在时 unstash 抛异常，
                // 整个 script 中断，allure 步骤被跳过，报告就消失了
                // '''               if (fileExists('reports/allure-results')){'''
                // unstash 'allure-results'
                // allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
                // ''' }'''
                try {
                    unstash 'allure-results'
                    if (fileExists('reports/allure-results')) {
                        allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
                    }
                } catch (Exception e) {
                    echo "跳过 Allure：未找到 allure-results stash（Playwright 阶段可能未成功）"
                }
            }
        }
    }
}
