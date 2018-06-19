Using
=====

This project is running at: http://ec2-54-202-87-225.us-west-2.compute.amazonaws.com/

The homepage has a sitemap with useful links as this doc itself, the admin, the endpoints and link to the github project.

This documentation is available at http://ec2-54-202-87-225.us-west-2.compute.amazonaws.com/docs/

To access de admin, use the URI http://ec2-54-202-87-225.us-west-2.compute.amazonaws.com/admin/ .

The api
-------

* Get bill Endpoint: 

  - URL: http://ec2-54-202-87-225.us-west-2.compute.amazonaws.com/call-records/get-bill/
  - Method: GET
  - GET Params args: source, period

* Get bill Endpoint:i
  - URL: http://ec2-54-202-87-225.us-west-2.compute.amazonaws.com/call-records/póst-record/
  - Method: POST
  - Post data args: type_record, call_id, source, destination, timestamp
