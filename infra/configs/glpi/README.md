# GLPI Configuration

This directory contains GLPI-specific configuration files.

## Initial Setup

When you first access GLPI at http://glpi.dockerwarts.local, you'll need to:

1. Select language
2. Accept license terms
3. Enter database connection:
   - SQL Server: `glpi-db`
   - SQL User: `glpi_user`
   - SQL Password: (from .env file)
   - Database: `glpidb`
4. Complete installation

## Default Credentials (first login)

After installation, use these default accounts:

- **Super-Admin**: glpi/glpi
- **Admin**: tech/tech
- **Normal**: normal/normal
- **Post-only**: post-only/post-only

⚠️ **IMPORTANT**: Change all default passwords immediately after first login!

## Configuration Files

Custom configuration files can be placed here and mounted into the GLPI container.

Example mounting in docker-compose.yml:
```yaml
volumes:
  - ./configs/glpi/config_db.php:/var/www/html/glpi/config/config_db.php:ro
```
