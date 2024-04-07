# Course Project - Entertaiment Center

This project is a course example to create a backend system using _object-oriented design_, _design patterns_, and some _good code practices_ in order to provide a __RESTful API__ with different services related to sports, courses, and one-day services in a generic entertaiment system.

## Business Model

This is a entertaiment center system where users could find information, buy courses, make reservations, among other, using a web platform or a mobile platform. The scope of the current project is to provide a set of services to be comsumed by different type of clients.

### Business Rules
  
- Clients just can schedule spaces between 8 am and 5 pm.
- A client just can schedule a space in the same space and hour.
- Payments must be just by electronic channels.

## User Stories

- __As a__ _manager_, __I want__ to see all schedulings of the week, __so what__ I can make decisions about publicity.
- __As a__ client, __I want__ to see the course catalog, __so what__ I can choose next vacations' course.
- __As a__ client, __I want__ to separate a sport space, __so what__ I can practice and be chill with friends.
- __As a__ client, __I want__ to pay courses and reservations using an online channel, __so what__ I can save time.
- __As a__ client, __I want__ to see prices for reservations, __so what__ I can choose the best option in price terms.
- __As a__ manager, __I want__ to have a report of payments by month, __so what__ I can make decisions about both spaces and courses definition.

## Technical Definitions

### Tools to Use

In this case, the backend will be build using _python 3.10_, and some related technologies as _Fast API_ to serve functionalities, _PyTest_ to apply some simple unit tests, and _Black_ to auto-format the code and increase code readibility.

## Entities

- Manager (User): generate reports(), create courses(), create publicities()
- Schedulling: day, hour, sport space[E], payment[E] 
- Publicity: text, deadline, hide()
- Client(User): make_reservations(), show_catalog()
- User:name, id, email, password, login(), logout()
- Course(Service): description, start_date, end_date, list_clients, add client(), remove client()
- Catalog Courses: list courses, add course(), remove course()
- Catalog Sport Spaces: list spaces, add space(), remove space()
- SportSpace (Service): location, dimensions
- Reservations: client[E], sport space [E], start date, end date
- PayChannel: name, description
- Payments: client, value, service[E]
- Service: name, price

# Processes

- Management Publicities:
  
![Activity Diagram](images/activity_management_publicities.png)

- View Schedulling Report:

- View Courses Catalog:

- Create a Reservation:

- Make Online Payment:

- View Payments Report: