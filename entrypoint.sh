#!/bin/bash

echo "Waiting for database..."
for i in {1..30}; do
  if python -c "import socket; s = socket.socket(); s.settimeout(2); s.connect(('db', 5432))" 2>/dev/null; then
    echo "Database started"
    break
  fi
  echo "Still waiting for database ('db:5432')..."
  sleep 2
done

python manage.py migrate

if [ "$DJANGO_ENV" = "development" ]; then
    echo "Development environment detected, seeding data..."
       python manage.py seed_data
fi

echo "Initialization complete"
