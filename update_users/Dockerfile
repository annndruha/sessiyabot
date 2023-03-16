# Marakulin Andrey @annndruha
# 2019

# Base image
FROM python:3.7.6-stretch

# Add the main dirictory
ADD ./ update_users/

# Set that dirictory
WORKDIR update_users

# Update Base image
RUN pip install --no-cache-dir -r requirements.txt

# Specify the port number the container should expose 
EXPOSE 1440

# Run the file
CMD ["python", "-u", "./update_users.py"]

# Example docker command:
# docker run -d --name update_users -v /root/update_users/config.py:/update_users/config.py imagename

# See logs:
# docker logs update_users --follow
