Dockgispy is a battery included docker image for the Gis Python Ecosystem, inspired by the QGISPY Battery Included Gis Python Module. The image was developed to solve the challenges beginners encounter while setting up Gis based Python Modules on different operating systems especially on Windows. Installing Python modules on Linux based operating system is easier and seamless, however this can be tedious and frustrating for new users and also experienced GIS users. With Dockgispy, users will only care about the execution of their workflows while the setting up processes is removed from the workflow. The image aims to be a low-code solution for deploying python GIS infrastructure for development and work. With a simple command, users have access to either a Jupyter Notebook or Jupyter Lab which is common with GIS Python Users for development and prototyping. 

**Tags**
- Smallest contains few GIS python module, intended for beginners, students or those who want to quickly prototype with basic GIS modules in Python. The installed libraries can be accessed here [link](https://github.com/Idowuilekura/dock_gis_py/blob/master/dockgispysmallest/requirements.txt). 
- Medium contains python modules from the smallest and more modules. This is intended for those who wish to explore GIS in python at an intermediate level. The installed libraries can be accessed here [link](https://github.com/Idowuilekura/dock_gis_py/blob/master/dockgispymedium/requirements.txt)
- Large contains python modules from the Medium image size and the inclusion of GDAL python module. The installed libraries can be accessed here [link](https://github.com/Idowuilekura/dock_gis_py/blob/master/dockgispylargest/requirements.txt)
- Largest Contains python modules from the Large with the inclusion of Apache Spark, a big data analytics tool for data processing and transformation. The installed python modules can be accessed here [link](https://github.com/Idowuilekura/dock_gis_py/blob/master/dockgispylargest/requirements.txt)

**Image Environment Variables**
To run the docker image, you need to provide two optional environment variables which are
1. The option to set the development environment to either open a Jupyter Notebook or Jupyterlab. This can be done with the *IDE_SET* environment variable, which expects either "lab" to start a jupyterlab or "notebook" to start a JupyterNotebook. You can choose to omit specifying the variable, however JupyterLab server will be started by default. 

**How to Run the Image**

Running docker images involves two methods:
1. Pulling the image before running the image as a container 
2. Running the image, which pulls the image automatically and run the image as a container. 
Dockgispy can also be run with either of the above methods. 
Both methods will be demostrated as shown below
    
    1. Pulling the image before running the image as a container. You can either pull the image with a tag which pulls the largest image tag by default or you pull with a tag 
        - Pulling without a tag, this pulls the largest image tag by default. The command to pull the image is shown below

            ```sh
            docker pull idowuilekura/dockgispy
            ```
        - Pulling the image with a tag of your choice. The command to pull the image with your specified tag is shown below

            ```sh
            docker pull idowuilekura/dockgispy:your_tag_name
            ```

        Once you are done, pulling the image, you need to run the image with this command and specify an optional argument which is the volume. port mapping and the development evironment of your choice. 
        - The `-v` command is needed to map the directory on the docker container with that on your local system. This ensures you can persit your work or operation (such as files created or notebook created) on the container to your local system. If you do not provide the option, any task will be lost once the container shuts down. The workdir on the container is `app`. Hence, to map a directory with name `work_dir` on your local system to the `app`, you need to do path_to_work_dir:app e.g `./work_dir:app` for relative path or pass the absolute path with `/home/pc/app:app`
        - The `-p` is a docker command to map the port on your system to that of the running container. You need to map any available port to port 8888 on the container. Jupyterlab and JupyterNotebook listens on port 8888 in the container. If you do not map the port on your system to that on the container, you will not be able to access the running instance of JupyterLab or Notebook in the container.
        - The `-e` command is for setting the development environment. To set the development platform, you can use -e IDE_SET=lab or IDE_SET=notebook to start JupyterLab or Notebook respectively. 
        
        To run the image you pulled without a tag, use the command below

            docker run idowuilekura/dockgis -v  path_to_your_folder:app -p port_number:8888
            
        To run the image you pulled with a tag, use the command below 
            
            docker run idowuilekura/dockgispy:prefered_tag -v path_to_your_folder:app -p port_number:8888
       
       After running the image, the container will start your preferred development environment on the terminal. If you omitted the SET_IDE environment variable, the default development environment will be JupyterLab. Once the development environment has started, you need to watch for a link similar to what is shown below which is used to access the jupyter server. 
        ```
        http://127.0.0.1:8888/lab?token=32962035228f06dcfc986f7b3baf89cb7fecbc346db418b5
        ```
        Copy the link and change `8888` to the port your chose while running the image. If your preferred port is `8000` then your updated link will be 
        ```
        http://127.0.0.1:8000/lab?token=32962035228f06dcfc986f7b3baf89cb7fecbc346db418b5
        ```
        Paste the link in your preferred web browser to access your preferred development environment. 
    2. Running the image, which pulls the image automatically and run the image as a container.
    To run the image without first pulling the image, you can use the below command, add the tag attribute if you want to automaticall pull and run a particular image. 
        ```
        docker run idowuilekura/dockgispy -v path_to_your_folder:app -p port_number:8888
        ```
**Running the Image with Docker Compose**

A much easier method to run the image is through a docker compose file. Docker-compose helps to automate the running of docker images. 
A sample docker compose file is shown below to run the smallest dockgispy image. If you are not familiar with docker-compose, you can read more with this [link](https://www.freecodecamp.org/news/what-is-docker-compose-how-to-use-it/). 

If you want to specify the environment variable, you can uncomment or remove the hash key behind the environment and the -IDE_SET=lab. 
Copy the belo, into a file with the name `docker-compose.yaml` and save it.

```
services:
  app:
    image: dockgispy:smallest
    container_name: dockgispycont
    # environment:
    #   - IDE_SET=lab
    ports:
      - "8000:8888"
    volumes:
      - ./app:/app
```
Once the file has been saved
