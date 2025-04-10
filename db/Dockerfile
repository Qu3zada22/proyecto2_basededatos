FROM postgres:14

# Copiar scripts SQL al directorio de inicialización
COPY 01_ddl.sql /docker-entrypoint-initdb.d/
COPY 02_data.sql /docker-entrypoint-initdb.d/

# Opcional: Configurar variables de entorno
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin123