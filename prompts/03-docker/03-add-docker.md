I want to run this application on container over a raspberry pi 4.

Create a Dockerfile to containerize this application. Put special focus on security. Run app with the minimum priviledges as possible. This application is going to save files on /app/content. I want to put extra security on that folder so nothing malicious can be executed there, but reading and writting files on that folder still possible to the application user.

Only application user can read and write on that folder, and nothing should be executed there.

Create a docker-compose that builds and runs frontend, backend and database. The application must be accessible on ports 80 (HTTP) and 443 (HTTPS). Use an nginx reverse proxy to expose these ports and route traffic to the frontend and backend services. The proxy should include self-signed SSL certificates for HTTPS out of the box; for production, custom certificates can be mounted to replace them.
