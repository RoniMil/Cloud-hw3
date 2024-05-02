A CI/CD pipeline for a service obtaining nutrition information from API Ninjas nutrition API.

The workflow triggers on PUSH and does the following jobs:

1. Build job - Creates a Docker image for the nutrition service.
2. Test job - Runs the image created in build in a container and uses pytest to run some tests on the dishes_meals service.
3. Query job - Issues nutrition requests to the service (invokes the api) based on the items in a file query.txt separated by newline.

Outputs:

1. A log file containing the time the workflow starts executing, my name, status of image building operation (successful/not successful), status of container running (runnning/not running) and status of pytest tests (successfull if all passed and failed if at least one failed)
2. Pytest tests results for each of the tests in assn3_tests.py
3. File response.txt that contains nutritional information for the items from query made in Query job.
4. The Docker image created in build job

Uploads outputs as artifacts after the workflow terminates
