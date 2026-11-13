
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checked out from GitHub.'
            }
        }

        stage('Verify Project Files') {
            steps {
                sh '''
                    echo "Checking project files..."

                    test -f frontend/index.html
                    test -f frontend/styles.css
                    test -f frontend/app.js

                    test -f backend/app.py
                    test -f backend/requirements.txt

                    echo "All required files are present."
                '''
            }
        }

        stage('Build Validation') {
            steps {
                sh '''
                    echo "Validating Python backend..."

                    python3 -m py_compile backend/app.py

                    echo "Backend syntax validation successful."
                '''
            }
        }

        stage('Deploy Frontend to S3') {
            steps {
                sh '''
                    aws s3 sync frontend/ s3://support-ticket-frontend-sidhu-2026/ --delete

                    echo "Frontend deployed successfully."
                '''
            }
        }

        stage('Invalidate CloudFront') {
            steps {
                sh '''
                    aws cloudfront create-invalidation \
                    --distribution-id E2SJOUTJPYZNM4 \
                    --paths "/*"

                    echo "CloudFront cache invalidation requested."
                '''
            }
        }

        stage('Deploy Backend to EC2') {
            steps {
                sh '''
                    echo "Deploying backend to EC2..."

                    sudo /usr/local/bin/deploy-support-ticket-backend

                    echo "Backend deployment completed."
                '''
            }
        }

        stage('Verify Backend') {
            steps {
                sh '''
                    sleep 3

                    curl --fail http://localhost:3000/health

                    echo "EC2 backend health check successful."
                '''
            }
        }
    }

    post {
        success {
            echo 'Frontend and backend deployment completed successfully!'
        }

        failure {
            echo 'Deployment failed. Check Jenkins Console Output.'
        }
    }
}
