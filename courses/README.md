# Courses 

This space have a set of materials for different courses, all focused on teaching _good practices_, _systems thinking approach_, _software development techniques_, all trying to solve _real-world problems_ using __Python__ programming language, and related tools.


- [Courses](#courses)
  - [How to Setup your Python Workspace](#how-to-setup-your-python-workspace)
  - [How to Setup required Tools](#how-to-setup-required-tools)
    - [Setup Local Git and GitHub Account](#setup-local-git-and-github-account)
      - [Installing Git on Windows](#installing-git-on-windows)
      - [Installing Git on Linux](#installing-git-on-linux)
      - [Setup Git Local Credentials](#setup-git-local-credentials)
      - [Creating a Project Folder with Git Client](#creating-a-project-folder-with-git-client)
    - [Installing Docker](#installing-docker)
      - [Installing Docker on Windows](#installing-docker-on-windows)
      - [Installing Docker on Linux](#installing-docker-on-linux)
  - [List of Courses](#list-of-courses)

***
***

## How to Setup your Python Workspace

It is strongly recommended to work with _Python 3.10_ or newer. Also, to use virtual environments to get the right isolated work environemnts.

In this sense, tools as __PyEnv__, __Poetry__, __PyTest__, will be used in all courses. For more information related to Python, and how to install/setup anything you need, you could go to [python course](python-for-everywhere/README.md)

***
***

## How to Setup required Tools

As computer engineer, you need to know powerful, useful, and state-of-the-art tools in order to give your best in both college and companies. So, here we will start to using _git_ and _docker_ to promove team work, and good practices to work collaboratively.

### Setup Local Git and GitHub Account

Git is a distributed version control system that allows multiple developers to collaborate on a project. It tracks changes to files and allows developers to work on different branches simultaneously. 

Git is important for team collaboration because it enables developers to work on the same codebase without overwriting each other's changes. It allows for easy collaboration, code review, and integration of changes from multiple team members. Git also provides a complete history of changes, making it easier to track and revert to previous versions if needed.

By using Git, teams can work together efficiently, manage code changes effectively, and ensure that everyone is working on the latest version of the code. It promotes transparency, accountability, and seamless integration of work done by different team members.

***

#### Installing Git on Windows

To install Git on Windows, you can follow these steps:

1. Visit the official Git [website](https://git-scm.com/downloads).Click on the __Download for Windows__ button to download the _Git installer_.
2. Once the download is complete, locate the downloaded file and double-click on it to run the installer.
3. Follow the instructions in the installer wizard. You can choose the default options or customize the installation according to your preferences.
4. During the installation, make __sure to select__ the option to _add Git to your system's PATH environment variable_. This will allow you to use __Git__ from the command line.
5. Complete the installation process by clicking on the __Finish__ button.

***

#### Installing Git on Linux

To install Git on Linux, you can use the package manager specific to your Linux distribution. Here are the instructions for Ubuntu/Debian:

1. Open a terminal. Run the following command to update the package lists:

```[bash]
sudo apt update
```

2. Run the following command to install Git:

```[bash]
sudo apt install git
```
 ***

#### Setup Git Local Credentials

Before you clone a repo in your machine, you need to setup your local Git username and email. This information will be used to identify your commits in the repository's history.

To set your Git username, open a terminal or PowerShell window and run the following command:
```[bash]
git config --global user.name "Your GitHUb User"
git config --global user.email "your-email-in-github@example.com"
```

If you want to use _SSH_ connection, recommended for secure connections, follow instructions in this [link](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

 

 #### Creating a Project Folder with Git Client

To create a folder using _mkdir_ and _clone a Git repository_ using _git remote add origin_ in a _PowerShell_ or _Terminal_ window, you can follow these instructions:

1. Open a PowerShell or terminal window. Navigate to the desired location where you want to create the folder using the _cd_ command. Once there, you could create the project folder using next command:

```[bash]
mkdir your-project
```

2. Navigate into the newly created folder using the _cd_ command. For example:

```[bash]
cd your-project
```

3. Set the remote origin for the cloned repository using the _git remote add origin_ command followed by the repository _URL_. For example:

```[bash]
git init
git remote add origin https://github.com/username/repository.git
```

4. Now, you can use _fetch_ command to download brances and repository information:

```[bash]
git fetch
```

5. Finally, to create branches to work, you could use next commands:

```[bash]
git checkout -b main
git pull origin main
git checkout -b your-dev-branh
git pull origin main
```

***

### Installing Docker

Docker is an open-source platform that allows you to automate the deployment, scaling, and management of applications using containerization. Containers are lightweight, isolated environments that package everything needed to run an application, including the code, runtime, system tools, and libraries. 

Docker simplifies the process of creating, distributing, and running applications by providing a consistent and reproducible environment. It allows developers to package their applications and dependencies into containers, which can then be deployed on any system that has Docker installed. This eliminates the "it works on my machine" problem and ensures that applications run consistently across different environments.

Docker is important for team collaboration because it enables developers to work on the same codebase using identical environments. Each developer can create a container with all the required dependencies and configurations, ensuring that everyone is working with the same setup. This reduces the chances of compatibility issues and makes it easier to share code and collaborate on projects.

***

#### Installing Docker on Windows

To install Docker and Docker Compose on Windows, you can follow these steps:

1. Visit the official Docker [website](https://www.docker.com/products/docker-desktop). Click on the __Download for Windows__ button to download the Docker installer.
2. Once the download is complete, locate the downloaded file and double-click on it to run the installer.
3. Follow the instructions in the installer wizard. You can choose the default options or customize the installation according to your preferences.
4. During the installation, __make sure__ to select the option _to enable Hyper-V_ if prompted. Docker requires Hyper-V to run containers on Windows.
5. Complete the installation process by clicking on the __Finish__ button.

***

#### Installing Docker on Linux

To install Docker and Docker Compose on Linux, you can use the following instructions for Ubuntu/Debian:
1. Open a terminal. Run the following command to update the package lists:

```[bash]
sudo apt update
```

2. Run the following command to _install_ __Docker__:

```[bash]
sudo apt install docker.io
```

3. After the installation is complete, start the __Docker__ service by running the following command:

```[bash]
sudo systemctl start docker
```

4. Run the following command to add your user to the __docker__ group, which will allow you to run Docker commands without using _sudo_:

```[bash]
sudo usermod -aG docker $USER
```

5. To install __Docker Compose__, run the following commands:

```[bash]
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

After following these instructions, Docker and Docker Compose should be installed and ready to use on both Windows and Linux systems.

***
***

## List of Courses

So, here there are some courses material, including python notebooks with code, slides, courses definitions, among others. You could dive in the folder _courses_ to explore specific courses and contents.

For now there is information for next courses:
1. [Advanced Programming](advanced-programming/README.md): related to object-oriented desing, template-controller-view model, and monoliths.
1. [Computer Networks](computer-netqorks/README.md): foundations of computer networking, devices, protocols, subnetting
1. [Databases Foundations](databases-foundations/README.md): Basic of DataBase design, ER model, relational databases, relational algebra.
1. [Python for Everyone](python-for-everyone/README.md): A set of notebooks with examples related to conditionals, loops, tuples, lists, dictionaries, anything useful to someone who wants to learn python.
1. [Software Modeling](advanced-programming/README.md): Not the best name, but this course is oriented to teach advandec topic of object-oriented design, including design patterns and good practices.
1. [Systems Analysis](advanced-programming/README.md): systems thinking, systems paradigms, swarm intelligence, IT projects management and leadership.
