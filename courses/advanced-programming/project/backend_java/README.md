# Backend Java Services

This is a set of services for user management, including authentication.
This __backend__ is based on _SprintBoot_ and _Maven_, as technologies to make a simple
both construction and deployment.

## Requirements

In order to run this code, you need to check next things in the _running machine_:
- Install _java jdk_. To chech this part run `java --version` into a terminal, and use at least __Java 17__.
- Install _Apache Maven_. To chech this part run `mvn --version` into a terminal, and use at least __Maven 3.6.3__.
- _[Optional]_ If you are using _VisualStudio Code_, install the __Java Extension Pack__ extension.
  
  
## How To Use

Create a first, could be empty, file with users information using next data structure:
```
[
    {
        "id": 1,
        "name": "John",
        "username": "john123",
        "password": "john_pass",
        "language": "english",
        "location": "USA",
        "age": 34,
    },
    {
        "id": 2,
        "name": "Jane",
        "username": "jane123",
        "password": "jane_pass",
        "language": "french",
        "location": "France",
        "age": 28
    }
]
```
The file must be placed into next path: `src/main/resources/data/users.json`.

There is to ways to run this one, both you should move to the root path of the project at any command line:
1. Execute since a terminal using:
- You could run `mvn clean-install` to add all the dependencies to the project.
- To execute the services and validate using localhost run `mvn spring-boot:run`.
2. Execute using docker:
- Create project image into docker, use next command: `docker -d -t ap_backend_java:1.0 .`.
- To validate if image was created into _Docker_, check using next command: `docker images`.  
- Execute image into a container using next command: `docker run  ap_backend_java ap_backend_java:1.0`
- To validate if container is running into _Docker_, check using next command: `docker ps`.

