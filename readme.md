Step1 : git clone https://github.com/ory/hydra.git
Step 2 : sudo docker-compose -f quickstart.yml \
    -f quickstart-postgres.yml \
    up --build
Step3 : git clone https://github.com/ipuneetgupta/hydra-openid.git
Step4 : touch .env
Step 5 :copy and paste this in .env 

        ADMIN_HYDRA_URL=http://localhost:4445
        PUBLIC_HYDRA_URL=http://localhost:4444
        AUTH_CLIENT_ID=videowiki
        AUTH_CLIENT_SECRET=aFHqO2~Ayz6d81KWs1ha.-6RtP

Step 5 : python3 manage.py makemigration & migrate
Step 6 : python3 manage.py runserver
step 7 : please change contrib/quickstart/5-min/hydra.yml 

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

Step 8: Enter this Url in browser
    
    http://127.0.0.1:4444/oauth2/auth?audience=&max_age=0&nonce=cbcvurctcddwfhzsnltwyz343&prompt=&redirect_uri=http://127.0.0.1:8000/api/token&response_type=code&scope=openid+offline&state=dsfssfsfsfsfslmksmf&client_id=videowiki

   

