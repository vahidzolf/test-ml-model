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
                    sh 'sudo  apt-get update &&  sudo apt-get install -y python3-pip'
                    sh 'sudo pip3 install docker-compose'
                    sh 'docker-compose -f ml-app.yml up &'
                }
            }
        }
    }
}
