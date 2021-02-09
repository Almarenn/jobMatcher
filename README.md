# resource_manager_service

### Build application
Build the Docker image manually by cloning the Git repo.
```
$ git clone https://github.com/eitanief/FlaskHomeAssignment.git
```
inside "FlaskHomeAssignment" folder:
```
$ docker build -t eitanief/resource_manager_service .
```

### Run the container
Create a container from the image.
```
$ docker run -it -p 7080:7080 eitanief/resource_manager_service

```

Notice that POST requests are designed to work with JSON body as argument



