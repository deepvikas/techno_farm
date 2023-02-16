
# Techno Farm

Techno Farm application is based on Rest api to store, get details and manupulate information regarding Farmers, farm associated to every Farmer, and detail related to their crops.

### Application have below feaures.

#### As a Admin:

* Admin can enroll himself for once.
* Can login/logout.
* Admin can add Details of Farmers.
* Admin can create records for Diffrent Type of Crops.
* Admin can create records of seasons.
* Admin can get the details of all farmer.
* Admin can search farmer on the basis of their firstname, lastname, farm, geolocation, address, city.
* Admin can delete any record of farmer.

#### As Farmer:

* Farmer can Make their accounts through signup.
* Farmer can login/logout.
* Farmer can update his profile, last name, password etc.
* Farmer can Add details about their Farms, one farmers can have multiple farms.
* Farmer can get the list of available crops.
* Farmer can get the list of all seasons.
* Farmer can add Crop to their farm.
* Farmer can also update the crop linked with specific farm.
* Farmer can get the information of all its farms.
* Farmer can get the information of any specific farm.
* Farmer can get the information of his profile.


Django Rest Framework is used to implement the above scenarios. All the operations mentioned above needs authentication and authorization on the basis of roles define.

Jwt token is used for authentication purpose, will will remain store in the cookies of client during its session.

sqlite3 db is used in this project as its a relational db.


#### Steps to Install and Run the application

* Install DjangoREST Framework.
* Clone this repo into your system.
* Go to techno_farm folder.
* Run command python3 manage.py makemigrations
* Run command python3 manage.py migrate
* Run commnad python3 manage.py runserver. (It will start the application)
* Now you can use the application's api by urls in your local or any server. Ex for local: http://127.0.0.1/signup (This end point required username and password key in the body of payload).
* You can use the Post collection attached with the application.


#### To optimize the api, apllication has following points.

* Minimize the response payload in case of any update or modication.
* Used pagitaion to limit no. of records send in response in single query.
* Used search params to search details of records on the basis of some conditions.
* Used patch methods to update the details.


#### Things we can do more for optimize the api.

* Can use caching for retrieving records.
* To scale the database we can use Mongo db to store the information of farmers in key value pair, as retrival from Mongo db is faster.
* We can use any Cloud base RDS to scale it.
* We can use any Service to restrict no. of hits on our api from a specific user or Ip.
