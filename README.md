# Building a Scalable Food Delivery Service Using ElasticSearch Geo Queries

In this repository you'll find the Django project shown in the Pycon 20 Colombia talk of the same title.

## Installation
Assuming you have installed **python3**, **docker**, **virtualenv** and **pip**:

* `git clone https://github.com/krsarmiento/pycon20.git`
* `cd pycon20/`
* `virtualenv /PATH/TO/ENV -p python3`. Preferably outside the project.
* `source /PATH/TO/ENV/bin/activate`
* `pip install -r requirements.txt`
* `docker-compose build`
* `docker-compose up`

The project runs at port 9000, while ElasticSearch does it at port 9200.

## Set Up
To upload the sample data go to `/lentti/elastic-setup`

## Dashboard
The dashboard displays a Google Map with polygons and a list of restaurants if found.
The url is `/lentti/dashboard`. You might specify the following query strings.

* `coordinates=6.209363,-75.5682937` to indicate a specific pair coordinates.
* `match_all=true` to retrieve all restaurants found without taking schedules into account.

## Google Maps
You'll need a Google Maps API KEY to make the map work properly. This key should be placed here:

```
//geofencing/dashboard.html

<script type="text/javascript"
  src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY">
</script>
```