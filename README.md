## Project name: Miniproject

#The mini project will work on the following aspects of Cloud applications#
    - REST-based service interface.
    - Interaction with external REST services.
    - Use of on an external Cloud database for persisting information.
    - Support for cloud scalability, deployment in a container environment.
    - Cloud security awareness.

#goal of the application#
The goal of this application is to build a prototype of a Cloud application.

#The miniproject compiles witht the following requirements#
  1. Provides a dynamically generated REST API. The API have a sufficient set of services for the selected application domain. The      REST API responses conform to the REST standards.
  2. the application makes use of an external REST service to complement itsfunctionality
  3. The application uses a cloud database for accessing persistent information.
  4. demonstartion of loadbalancing and scaling of application
    - E.g. Kubernets based load balancing as well as Cassandra ring scaling)

## set region and zone for new cluster
gcloud config set compute/zone europe-west2-b
export PROJECT_ID="$(gcloud config get-value project -q)"

## Set up a single node Cassandra inside a docker container 

## Pull the Cassandra Docker Image
docker pull cassandra:latest


## Create Cassandra Instance within Docker and check if the instance is running correctly
docker run --name cassandra-test -d cassandra:latest
docker ps

## Get csv file from github
wget -O beers.csv https://raw.githubusercontent.com/aak36/miniproject/master/beers.csv

## Copy the data into the container
docker cp beers.csv cassandra-test:home/beers.csv

## Activate cqlsh inside the Docker container
docker exec -it cassandra-test cqlsh

## create keyspace
CREATE KEYSPACE beers WITH REPLICATION = {'class' : 'SimpleStrategy' , 'replication_factor' : 1};

## create table
CREATE TABLE beers.data( ID int, Name text PRIMARY KEY, tagline text);

## copy data from csv into the database
COPY beers.data(id, name, tagline) FROM '/home/beers.csv' WITH DELIMITER=',' AND HEADER=TRUE;
select * from beers.data;

## Test the data with querie
select * from beers.data;

## Create 3 Node Cluster for Cassandra
gcloud container clusters create cassandra --num-nodes=3 --machine-type "n1-standard-2"

## Define a service using three files
wget -O cassandra-peer-service.yml http://tinyurl.com/yyxnephy
wget -O cassandra-service.yml http://tinyurl.com/y65czz8e
wget -O cassandra-replication-controller.yml http://tinyurl.com/y2crfsl8

## After the files are downloaded run the three components
kubectl create -f cassandra-peer-service.yml
kubectl create -f cassandra-service.yml
kubectl create -f cassandra-replication-controller.yml

## check that the single container is running correctly
kubectl get pods -l name=cassandra

## If the container is running correctly you can scale up the numbers of nodes via replication-controller
kubectl scale rc cassandra --replicas=3

## Pick one of the containers and check if the ring is formed
kubectl exec -it cassandra-cvq5h -- nodetool status

## Use the same container and copy the data from the previous section
kubectl cp beers.csv cassandra-cvq5h:/beers.csv

## run cqlsh inside the container
kubectl exec -it cassandra-cvq5h cqlsh



