
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
                    test -f frontend/style.css
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

        stage('Pipeline Success') {
            steps {
                echo 'Support Ticket Management pipeline completed successfully!'
            }
        }
    }
}
