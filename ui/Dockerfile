# Use Node 18 Alpine
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 5173

# Run in development mode (easiest for local deployment without Nginx setup)
# --host 0.0.0.0 is required for Docker networking
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
