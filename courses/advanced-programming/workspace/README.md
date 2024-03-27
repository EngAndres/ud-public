# Course Workspace

You should have python and docker installed in your machine as prerequisite to use next workspace.

Here the idea is to provide you a clean and beautiful environment to work in your course project. As the idea is to standarize using simple _DevOps_ concepts, here a couple of folders are define, for _backend_ and _frontend_ respectivaly.

Also, based on those folders, _Dockerfiles_ are defined in order to make easy-automate deployments using a _docker-compose_ file which includes a _postgresql_ database.

Some _requirements_ files are defined in order to separate the required libraries for each stage, and also a _Makefile_ is created in order to provide you simple command-line options to make easier installations and quality verification.

## How to Use

Just copy the contents of this folder into the root of your project repository, and organize your project code into _backend_ and _frontend_ folders. Then, since your machine you could run commands in order to deploy your project.

You must open your command-line, and move to the root of your project. There, you must activate your python virtual environment. If you want to install all requirements to develop your project, you could run:
```[bash]
make install
```