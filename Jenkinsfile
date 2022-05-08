pipeline
{
    agent any
    stages
    {
        stage('Train model')
        {
            agent { label 'master' }
            steps
            {
                script
                {
                  sh '. sklearn-venv/bin/activate'
                  sh 'pip install -r requirements.txt '
                  sh 'python train.py'
                }
            }
        }
        stage('Build docker image and run app')
        {
            agent { dockerfile true }
            steps
            {
                script
                {
                    sh "echo 'Hello!!' "
                }
            }
        }
    }
}
