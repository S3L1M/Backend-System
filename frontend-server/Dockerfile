# Use the official Nginx image as the base image
FROM nginx:latest

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf || true

# Copy your custom Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d

# Copy your HTML files to the appropriate directory
COPY html /etc/nginx/html

# Expose the default Nginx port
EXPOSE 80

# Start Nginx when the container is run
CMD ["nginx", "-g", "daemon off;"]
