# Production deployment script
#!/bin/bash

# Exit on error
set -e

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    exit 1
fi

# Load environment variables
source .env

# Check required variables
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "Error: OPENROUTER_API_KEY not set in .env file"
    exit 1
fi

if [ -z "$DOMAIN" ]; then
    echo "Error: DOMAIN not set in .env file"
    exit 1
fi

# Create necessary directories
mkdir -p certbot/conf certbot/www

# Replace domain in nginx config
sed -i "s/yourdomain.com/$DOMAIN/g" nginx/nginx.prod.conf

# Build and start services
export VERSION=$(git describe --tags --always)
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Initialize SSL certificate
docker-compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path /var/www/certbot \
    --email admin@$DOMAIN \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# Reload nginx to apply SSL configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload

echo "Deployment complete! Application is running at https://$DOMAIN"
