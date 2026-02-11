Add to openapi contract and fastapi endpoints two new endpoints to handle artist and stands. People can fill a form to participate, so I want to get that information. Would be very basic, you can see information on artist.png

Endpoints should like:

1. POST "/api/v1/artist" - Register a new artist
2. POST "/api/v1/stand" - Register a new stand

Create also a GET for each object, artist and stand so I can read what we have on db.