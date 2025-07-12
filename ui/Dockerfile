# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including dev dependencies needed for build)
RUN npm install

# Copy app files
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine

# Install runtime dependencies
RUN apk add --no-cache curl

# Copy built app from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]