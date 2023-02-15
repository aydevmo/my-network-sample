The objective of this project is to run Ansible in Windows environment. Ansible is designed for Linux. Although one can run it on Windows in WSL (Windows Subsystem for Linux) environment, managing the packages and dependencies is a hassle. 
     
Some people run Ansible in docker containers, and I think it’s a good project idea. We’d need to use bind mounts to share folders between Windows host and Linux in Docker containers. This would also allow us to conveniently check in Ansible runbooks to GitHub using Visual Studio Code on Windows host.
