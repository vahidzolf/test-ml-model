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
                  sh 'python -m venv sklearn-venv; . sklearn-venv/bin/activate; pip install -r requirements.txt; python train.py'
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
