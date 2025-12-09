FROM openjdk:17-ea-17-jdk-slim

WORKDIR /app

COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .

RUN chmod +x ./mvnw

# install dependencies
RUN ./mvnw dependency:go-offline -B

# current app
COPY src ./src
RUN ./mvnw clean package -DskipTests

EXPOSE 8080
CMD ["java", "jar", "target/medical-exams-0.0.1-SNAPSHOT.jar"]