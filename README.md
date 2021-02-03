# freelancing-portal

Pre-reqs:
1. make sure you have docker=20.10.2 and docker-compose=1.27.4 installed on your system
2. disable any local server currently listening at port 80 on the machine

How to run:
1. open the terminal

2. cd to the main project directory

3. run the command "make run"
   or run command "bash run_docker.sh" if make is not available

4. open http://localhost (or http://server-address) in your browser

P.S.
1. if "make run" was used, run command "make stop" to stop 
   existing containers, if required
2. to run a simple flask dev server, cd into the "app" sub-dir, manually 
   create a virtual-environment using 'requirements.txt' file and finally 
   run "python run.py" from inside the environment
