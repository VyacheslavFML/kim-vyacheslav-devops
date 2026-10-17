pipeline {
    agent any
    options { skipDefaultCheckout(true); timestamps(); disableConcurrentBuilds() }
    environment {
        STUDENT_NAME = 'Vyacheslav'
        STUDENT_SURNAME = 'Kim'
        STUDENT_GROUP = 'IT2-2312'
        STUDENT_ID = '37746'
        IMAGE = 'kim-vyacheslav-devops'
        CONTAINER = 'kim-vyacheslav-container'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --format="Commit: %H%nSubject: %s"'
                echo "Student: ${STUDENT_NAME} ${STUDENT_SURNAME}\nGroup: ${STUDENT_GROUP}\nStudent ID: ${STUDENT_ID}"
            }
        }
        stage('Build') {
            steps { sh 'python3 -m compileall -q app' }
        }
        stage('Test') {
            steps { sh 'python3 -m unittest discover -s tests -v' }
        }
        stage('Docker Build') {
            steps { sh 'docker build -t "$IMAGE" . && docker images "$IMAGE"' }
        }
        stage('Docker Run') {
            steps {
                sh '''
                    if docker container inspect "$CONTAINER" >/dev/null 2>&1; then
                        docker rm -f "$CONTAINER"
                    fi
                    docker run -d --name "$CONTAINER" -p 127.0.0.1:8081:8080 \
                      -e STUDENT_NAME -e STUDENT_SURNAME -e STUDENT_GROUP -e STUDENT_ID "$IMAGE"
                    ready=0
                    for attempt in $(seq 1 30); do
                        if docker exec "$CONTAINER" python -c 'import urllib.request,json,os; d=json.load(urllib.request.urlopen("http://localhost:8080/student")); assert d["Student ID"]==os.environ["STUDENT_ID"]; print(d)'; then
                            ready=1; break
                        fi
                        sleep 1
                    done
                    test "$ready" = 1
                    docker logs "$CONTAINER"
                    docker ps --filter name="$CONTAINER"
                '''
            }
        }
    }
    post { always { echo "Pipeline result: ${currentBuild.currentResult}" } }
}
