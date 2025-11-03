FROM node:20-alpine3.19

# Set working directory
WORKDIR /app

# Install dependencies (production only)
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Run the app
CMD ["node", "app.js"]