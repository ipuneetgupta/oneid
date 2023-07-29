# OneID - Unified Identity for Microservices

OneID is a project that aims to provide a unified identity and single sign-on solution for microservices using Hydra, a cloud-native OAuth 2.0 and OpenID Connect server.

## Prerequisites

Before proceeding, make sure you have the following installed:

- Git
- Docker
- Python 3
- PostgreSQL (or you can use Dockerized PostgreSQL)

## Installation

### Step 1: Clone Hydra Repository

```bash
git clone https://github.com/ory/hydra.git
```

Step 2: Start Hydra

```bash 
cd hydra
sudo docker-compose -f quickstart.yml -f quickstart-postgres.yml up --build
```

Step 3: Clone OneID Repository

```bash 
git clone https://github.com/ipuneetgupta/hydra-openid.git
```

Step 4: Create .env File

```bash
touch .env
```

Step 5: Configure .env File
Copy and paste the following environment variables into the .env file:

```bash
ADMIN_HYDRA_URL=http://localhost:4445
PUBLIC_HYDRA_URL=http://localhost:4444
AUTH_CLIENT_ID=videowiki
AUTH_CLIENT_SECRET=aFHqO2~Ayz6d81KWs1ha.-6RtP
```

Save and close the .env file.

Make sure to replace the placeholder values (ADMIN_HYDRA_URL, PUBLIC_HYDRA_URL, AUTH_CLIENT_ID, and AUTH_CLIENT_SECRET) with appropriate and secure values for your specific configuration. These environment variables will be used by the OneID server to interact with the Hydra server for authentication and authorization purposes.


Step 6: Apply Database Migrations
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Step 7: Run the OneID Server
```
python3 manage.py runserver
```

Step 8: Update Hydra Configuration
Modify the hydra.yml file located at contrib/quickstart/5-min/hydra.yml in the Hydra repository to include the following changes:
```
serve:
  cookies:
    same_site_mode: Lax

  urls:
    self:
      issuer: http://127.0.0.1:4444
    consent: http://127.0.0.1:8000/api/consent
    login: http://127.0.0.1:8000/api/login
    logout: http://127.0.0.1:8000/api/logout

  secrets:
    system:
      - youReallyNeedToChangeThis

  oidc:
    subject_identifiers:
      supported_types:
        - pairwise
        - public
      pairwise:
        salt: youReallyNeedToChangeThis
```

Step 9: Start OneID Authentication
Open the following URL in your web browser:

`http://127.0.0.1:4444/oauth2/auth?audience=&max_age=0&nonce=cbcvurctcddwfhzsnltwyz343&prompt=&redirect_uri=http://127.0.0.1:8000/api/token&response_type=code&scope=openid+offline&state=dsfssfsfsfsfslmksmf&client_id=videowiki`

## Usage
With the OneID server running, your microservices can now authenticate users using the OpenID Connect flow. When users access a protected microservice, they will be redirected to the OneID server for authentication. Once authenticated, they will be redirected back to the microservice with the necessary tokens.

## Note
Remember to replace the placeholder values in the .env file and the Hydra configuration with appropriate and secure values for your production setup. Additionally, consider securing sensitive information like secrets and client credentials using appropriate methods.

## Credits
OneID is built on top of Hydra, an open-source project developed by Ory.

## Authors

- **Puneet Gupta**

## License
This project is licensed under the MIT License. Feel free to contribute and enhance the project!

## Acknowledgments

If your project is built on the work of other developers, organizations, or libraries, acknowledge them here.



