I want to create a Python, FastAPI API project to handle database diagram on image db.png. I want to use poetry as a package manager.

For database, use MySQL connector.

You should implement these endpoints that always use JSON for communication:

1. POST "/api/v1/login" - That allow user to authenticate using Google SSO.
2. POST "/api/v1/singup" - That create an user on DB. I want to handle this user creation using Google SSO. I dont want to store any kind of password. Check if another column should be on database to handle this in as much as cleaner and standard way as possible.
3. POST "/api/v1/category/{category_id}/partitipate - That would receive a JSON with the participation. This participation object will have the userId, categoryId, description and a list of files. These file should be saved on disk on a preconfigured path. File structure would be category_name > participant_name > file_01, file_02...
4. GET "/api/v1/category - List of categories
5. GET "/api/v1/category/{categoryId}/participant" - List of participant by category
6. GET "/api/v1/participant" - List of users that are on participant table.
7. GET "/api/v1/votes - List of participations with a count of votes by category
8. POST "/api/v1/category/{categoryId}/participant/{participantId}/vote - Receive a JSON with userId. This would generate a new vote on InitialVote table. It's important to validate that user has not voted already for this category.

Important note, create a openapi latest stable version contract.

Not all endpoints are going to be accesible for everybody, I want to have on JWT token a group for admins that allow run some endpoints.

Admin endpoints are:

GET /api/v1/category/{categoryId}/participant
GET "/api/v1/participant
GET "/api/v1/votes
