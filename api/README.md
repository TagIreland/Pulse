# api — the Spring Boot service

```bash
./mvnw spring-boot:run
curl http://localhost:8080/api/sessions
```

`./mvnw` missing? Run `mvn -N wrapper:wrapper` once and commit the result.

## Where things are

```
session/SessionController.java   accepts the HTTP request, returns a result
session/SessionRepository.java   where the data comes from (hardcoded until Day 2)
session/Session.java             what goes over the wire as JSON
config/WebConfig.java            CORS. You will be back here on Day 1.
resources/application.properties configuration, including the Day 2 database switch
```

## The layers, and why anyone cares

A request arrives at the **controller**, which knows about HTTP and nothing else. It
asks a **repository**, which knows about the database and nothing about HTTP. If your
project grows a real service layer, that sits between them and holds logic that is
neither.

You can absolutely put a SQL query in a controller and it will work. The reason not to
is that six months later somebody needs the same number somewhere else, copies the
query, and one of the two copies gets fixed.
