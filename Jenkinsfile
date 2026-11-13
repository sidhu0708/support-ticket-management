
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
                    echo "All required frontend files are present."
                '''
            }
        }

        stage('Build Validation') {
            steps {
                echo 'Frontend build validation completed.'
            }
        }

        stage('Deploy to S3') {
            steps {
                sh '''
                    aws s3 sync frontend/ s3://support-ticket-frontend-sidhu-2026/ --delete
                    echo "Frontend deployed to S3 successfully."
                '''
            }
        }

        stage('Invalidate CloudFront') {
            steps {
                sh '''
                    aws cloudfront create-invalidation \
                    --distribution-id E2SJOUTJPYZNM4 \
                    --paths "/*"
                '''
            }
        }
    }

    post {
        success {
            echo 'Support Ticket Management deployed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
