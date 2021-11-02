# Education NUC Setup



## Prerequisite
**Install basic tools** 
```
$ sudo apt install -y build-essential software-properties-common vim terminator net-tools htop make git geany git-doc gitk samba samba-common openssh-server screen tree font-manager
```
**Install Google Chrome**
```
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo apt install ./google-chrome-stable_current_amd64.deb
```
**Install pip**
```
$ sudo apt install python3-pip
$ sudo pip3 install --upgrade pip
```

## Install Requirements.txt

```
$ cd ~/home/intel/training
$ sudo pip3 install -r requirements.txt
```
The installation may stop during the process due to **pexpect** and **pyyaml** package errors. If so run:
```
$ sudo pip3 install --ignore-installed pexpect
$ sudo pip3 install --ignore-installed pyyaml
$ sudo pip3 install -r requirements.txt
```


## Install OpenVINO

1. Follow instructions at: https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_apt.html and install OpenVINO (install the dev version not the runtime version)
2. OpenVINO version should be **2021.4.689**.

## Install Docker and Docker-Compose

 1. Follow instructions at: https://docs.docker.com/engine/install/ubuntu and install Docker
 2. Add User to Docker group
 ```
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
 ```
 3. Reboot the system for the update to take place
 4. Follow instructions at: https://docs.docker.com/compose/install and install Docker-Compose


## Install EII

1. Follow instructions at: https://www.intel.com/content/www/us/en/develop/documentation/edge-insights-industrial-doc/get-started-guide/install-edge-insights-for-industrial.html and install EII.
2. EII version should be **2.6**.
3. Then follow up with the commands below:
```
$ cd IEdgeInsights/build
$ cp usecases/video-streaming.yml usecases/video-webstreaming.yml
$ vim usecases/video-webstreaming.yml #(Then remove VideoIngestion)
$ vim .env #(Then change DEV_MODE=true)
$ python3 ./builder.py -f usecases/video-webstreaming.yml #May be required to "pip3 install ruamel_yaml"
$ docker-compose -f docker-compose-build.yml build
$ docker-compose up
```


## Additional Setup
• **apt install**
```
$ sudo apt install meld
$ sudo apt install net-tools
$ sudo apt install v4l-utils
$ sudo apt install virtualenv
```
• **OpenVINO**
```
$ ./opt/intel/openvino_2021/deployment_tools/model_optimizer/install_prerequisites/install_prerequisites_tf.sh
$ ./opt/intel/openvino_2021/install_dependencies/install_NEO_OCL_driver.sh
```
•	**LPR (License Plate Recognition)**
1. Go to /home/intel/training/Day.03-OpenVINO-Smart_Toll_Gate
  ```
$ cd /home/intel/training/Day.03-OpenVINO-Smart_Toll_Gate
  ```
2. Install openvino training extensions
  ```
$ git clone https://github.com/openvinotoolkit/training_extensions
$ cd training_extensions
  ```
3. Apply the following patch
  ```
$ git am ../RES/0001-kor-patch.patch
  ```
4. Clone and checkout state of tensorflow/models:
```
$ git clone https://github.com/tensorflow/models.git $(git rev-parse --show-toplevel)/external/models
$ cd $(git rev-parse --show-toplevel)/external/models
$ git checkout f0899f18e178afb4b57c50ec32a7e8952e6f6a99
$ cd -
  ```
5. Create and activate virtual environment:
  ```
$ cd $(git rev-parse --show-toplevel)/misc/tensorflow_toolkit/lpr
$ virtualenv venv -p python3.6 --prompt="(lpr)"
$ echo "source /opt/intel/openvino_2021/bin/setupvars.sh" >> venv/bin/activate
$ source venv/bin/activate
  ```
6. Install the modules
  ```
$ CPU_ONLY=true pip3 install -e .
$ pip3 install -e ../utils
  ```
 
• **CVAT**
1. Follow instructions at: https://openvinotoolkit.github.io/cvat/docs/administration/basics/installation/ and install CVAT
2. Create superuser by executing the follow command:
```
$ docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'
> admin / intel123
```

## Execution 

* Run the following command on the root directory of the project to set the environment variables and execute jupyter notebook 

```bash
$ ./launch_jupyter.sh 
```
