# Stage 1: Build
# Use Node 20 Alpine for smaller image size
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build for production
RUN npm run build

# Stage 2: Production
# Use nginx alpine for lightweight serving
FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built application from builder stage
# Angular 20 with @angular/build outputs to dist/{project-name}/browser
COPY --from=builder /app/dist/angular2/browser /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
