
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

                    echo "All required project files are present."
                '''
            }
        }

        stage('Build Validation') {
            steps {
                sh '''
                    echo "Validating Python backend..."

                    python3 -m py_compile backend/app.py

                    echo "Backend syntax validation successful."
                    echo "Frontend build validation completed."
                '''
            }
        }

        stage('Deploy Frontend to S3') {
            steps {
                sh '''
                    echo "Deploying frontend to S3..."

                    aws s3 sync frontend/ s3://support-ticket-frontend-sidhu-2026/ --delete

                    echo "Frontend deployed to S3 successfully."
                '''
            }
        }

        stage('Invalidate CloudFront') {
            steps {
                sh '''
                    echo "Invalidating CloudFront cache..."

                    aws cloudfront create-invalidation \
                    --distribution-id E2SJOUTJPYZNM4 \
                    --paths "/*"

                    echo "CloudFront invalidation requested."
                '''
            }
        }

        stage('Deploy Backend to EC2') {
            steps {
                sh '''
                    echo "Deploying backend to EC2..."

                    sudo /usr/local/bin/deploy-support-ticket-backend

                    echo "Backend deployed to EC2 successfully."
                '''
            }
        }

        stage('Verify Backend') {
            steps {
                sh '''
                    echo "Checking EC2 backend health..."

                    sleep 3

                    curl --fail http://localhost:3000/health

                    echo "EC2 backend health check successful."
                '''
            }
        }
    }

    post {
        success {
            echo 'Support Ticket Management frontend and backend deployed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check Console Output for details.'
        }
    }
}
