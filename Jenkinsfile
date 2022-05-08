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
            steps
            {
                script
                {
                    sh 'apt-get update &&  apt-get install -y python3-pip'
                    sh 'pip3 install docker-compose'
                    sh 'docker-compose -f ml-app.yml build '
                }
            }
        }
    }
}
