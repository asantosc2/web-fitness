#!/bin/bash
echo "🔄 Exportando base de datos..."
docker exec -t web-fitness-back-db-1 pg_dump -U postgres web_fitness > backup.sql
echo "✅ Backup guardado como backup.sql"

# sh app/scripts/exportar_datos.sh 
# docker exec -t web-fitness-back-db-1 pg_dump -U postgres web_fitness > backup.sql


