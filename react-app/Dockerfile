# Dockerfile
FROM node:20

WORKDIR /app

# Copy the rest of the application files  
COPY . .  

# Install project dependencies  
RUN npm install  

# Expose the port the application will run on  
EXPOSE 5173 

# Define the command to run the application  
CMD ["npm", "run", "dev", "--", "--host"]