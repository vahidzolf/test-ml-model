//def ADMIN_SCRIPT_BRANCH = "NRRPLT-8138-deploy-developers-docker-image"

pipeline
{
    agent any
    environment
    {
//         NRP_USER = 'bbpnrsoa'
//         NRP_GROUP= 'bbp-ext'
//         NRP_NUM_PROCESSES = 8
//         NRP_SOURCE_DATE = '2017-08-17 16:30'
//         NexusDockerRegistryUrl = "${env.NEXUS_REGISTRY_IP}:${env.NEXUS_REGISTRY_PORT}"
//         ROS_ETC_DIR='/opt/ros/noetic/etc/ros'
//         branch_tag=defineTag(params.BRANCH_NAME, params.BASE_BRANCH_NAME, params.NRP_DOCKER_REF_BRANCH, params.ADMIN_SCRIPT_BRANCH)
//         deploy_env = selectEnv(env.JOB_NAME, params.env, params.arbitrary_env)
//         deploy_key = "${env.deploy_env == env.JOB_NAME.tokenize('_')[0] ? (env.deploy_env + '_key') : env.DEPLOY_TEST_KEY}"
    }

    stages
    {
        stage('Train model')
        {
            steps
            {
                script
                {
                  sh 'source sklearn-venv/bin/activate'
                  sh 'pip3 install -r requirements.txt '
                  sh 'python train.py'
                }
            }
        }
        stage('Build docker image for app')
        {
            steps
            {
                script
                {
                    sh "docker tag nrp:dev ${NexusDockerRegistryUrl}/nrp:${branch_tag}"
                    sh "docker tag hbpneurorobotics/nrp_proxy:dev ${NexusDockerRegistryUrl}/nrp_proxy:${branch_tag}"
                    sh "docker tag hbpneurorobotics/nrp_frontend:dev ${NexusDockerRegistryUrl}/nrp_frontend:${branch_tag}"
                    sh "docker push ${NexusDockerRegistryUrl}/nrp:${branch_tag}"
                    sh "docker push ${NexusDockerRegistryUrl}/nrp_proxy:${branch_tag}"
                    sh "docker push ${NexusDockerRegistryUrl}/nrp_frontend:${branch_tag}"
                    sh 'docker logout ${NexusDockerRegistryUrl}'
                }
            }
        }
        stage('Deploy with ansible')
        {
            parallel
            {
                stage('Deploy backend')
                {
                    when
                    {
                        expression { return params.DEPLOY_IMAGE }
                    }
                    steps
                    {
                        script
                        {
                            dir('admin-scripts')
                            {
                                withCredentials([ \
                                        usernamePassword(credentialsId: 'nexusadmin', usernameVariable: 'USER', passwordVariable: 'PASSWORD'), \
                                        sshUserPrivateKey(credentialsId: "${env.deploy_key}", keyFileVariable: 'USER_KEY_PATH') ])
                                        {
                                        //update backends first
                                        ansiblePlaybook(credentialsId: "${env.deploy_key}", \
                                                        colorized: true, inventory: 'ansible/hosts', \
                                                        playbook: 'ansible/update.yml', \
                                                        limit : "${env.deploy_env}_backends", \
                                                        become : true , \
                                                        forks : 20, \
                                                        extraVars: [docker_tag :  "${branch_tag}" , \
                                                                    docker_reg : "${NexusDockerRegistryUrl}", \
                                                                    docker_user :  '$USER', \
                                                                    docker_pass :  '$PASSWORD' , \
                                                                    ansible_python_interpreter: '/usr/bin/python3' ] )

                                        //keep_running backends
                                        ansiblePlaybook(credentialsId: "${env.deploy_key}", \
                                                        colorized: true, inventory: 'ansible/hosts', \
                                                        playbook: 'ansible/keep_running.yml',  \
                                                        limit : "${env.deploy_env}_backends",  \
                                                        become : true ,  \
                                                        forks : 20, \
                                                        extraVars: [docker_tag :  "${branch_tag}" , \
                                                                    docker_reg : "${NexusDockerRegistryUrl}",  \
                                                                    force_config: "true" ,  \
                                                                    ansible_python_interpreter: '/usr/bin/python3' ] )
                                        }
                            }
                        }
                    }
                }
                stage('Deploy frontend')
                {
                    when
                    {
                        expression { return params.DEPLOY_IMAGE }
                    }
                    steps
                    {
                        script
                        {
                            dir('admin-scripts')
                            {
                                withCredentials([ \
                                        usernamePassword(credentialsId: 'nexusadmin', usernameVariable: 'USER', passwordVariable: 'PASSWORD'), \
                                        sshUserPrivateKey(credentialsId: "${env.deploy_key}", keyFileVariable: 'USER_KEY_PATH') ])
                                        {


                                        //update frontend
                                        ansiblePlaybook(credentialsId: "${env.deploy_key}", \
                                                        colorized: true, inventory: 'ansible/hosts', \
                                                        playbook: 'ansible/update.yml',  \
                                                        limit : "${env.deploy_env}_frontend", \
                                                        become : true ,  \
                                                        extraVars: [docker_tag :  "${branch_tag}" , \
                                                                    docker_reg : "${NexusDockerRegistryUrl}", \
                                                                    docker_user :  '$USER', \
                                                                    docker_pass :  '$PASSWORD', \
                                                                    ansible_python_interpreter: '/usr/bin/python3' ] )

                                        //keep_running frontend
                                        ansiblePlaybook(credentialsId: "${env.deploy_key}",  \
                                                        colorized: true,  \
                                                        inventory: 'ansible/hosts', \
                                                        playbook: 'ansible/keep_running.yml', \
                                                        limit : "${env.deploy_env}_frontend",  \
                                                        become : true ,  \
                                                        extraVars: [docker_tag :  "${branch_tag}" , \
                                                                    docker_reg : "${NexusDockerRegistryUrl}", \
                                                                    force_config: "true" ,  \
                                                                    ssh_key_path: '${USER_KEY_PATH}', \
                                                                    ansible_python_interpreter: '/usr/bin/python3' ] )
                                        }
                            }
                        }
                    }
                }
            }
        }

    }
}
