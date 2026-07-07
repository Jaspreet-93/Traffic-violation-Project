# Build stage
FROM node:20-alpine AS build-stage

WORKDIR /app

# Copy package descriptors
COPY package*.json ./

# Install packages
RUN npm ci

# Copy all source files
COPY . .

# Build Vite application static files
RUN npm run build

# Production stage
FROM nginx:stable-alpine AS production-stage

# Copy compiled SPA static assets to Nginx default document root
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
