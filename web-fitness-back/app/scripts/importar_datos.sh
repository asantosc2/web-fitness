#!/bin/bash
if [ ! -f backup.sql ]; then
  echo "❌ No se encontró el archivo backup.sql"
  exit 1
fi

echo "📥 Restaurando base de datos desde backup.sql..."
docker exec -i web-fitness-back-db-1 psql -U postgres web_fitness < backup.sql
echo "✅ Restauración completada"