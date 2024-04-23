FROM eclipse-mosquitto


# Mosquitto Requires those files to have certain permissions
# Git does not like not having read / write access to some files
# So we copy them top our custom image and fix the permissions.
COPY config/mosquitto.conf /mosquitto/config/mosquitto.conf 
COPY config/pwfile /mosquitto/config/pwfile  

RUN chmod 0700 /mosquitto/config/mosquitto.conf
RUN chmod 0700 /mosquitto/config/pwfile 

