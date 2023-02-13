# Original command: docker run -it --name aydevmo_ansible --mount type=bind,source=c/_vscode/my-network-sample/automation/ansible/ansible_docker_01_bind_mounts/,target=/home/ansible/ ansible 

$ContainerName = 'aydevmo_ansible_01'
$MyMountDest = '/home/ansible'

$MyMountSrc = $PSScriptRoot.Replace('\', '/').Replace('C:','c')
$MyMountSrc = $MyMountSrc.Replace('/ansible_docker_01','/ansible_docker_01_bind_mounts')

$DockerPsa = docker ps -a

$DockerPs  = docker ps

if( $DockerPs -match $ContainerName ){
    # if the container is running.
    "Option #1"
    docker exec -it $ContainerName /bin/bash
}
elseif( $DockerPsa -match $ContainerName ){
    # if the container exited.
    "Option #2"
    docker restart $ContainerName
    docker exec -it $ContainerName /bin/bash
}
else {
    # if there is no container yet.
    "Option #3"
    docker run -it --name $ContainerName --mount type=bind,source=$MyMountSrc,target=$MyMountDest ansible 
}
