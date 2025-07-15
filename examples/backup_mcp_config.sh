#!/bin/bash
# MCP Config Backup Script
# This script creates a backup of the Amazon Q MCP configuration file with a date suffix

# Configuration
SOURCE_FILE="/home/ec2-user/.aws/amazonq/mcp.json"
BACKUP_DIR="/home/ec2-user/mcp_backups"
RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Get current date in YYYYMMDD format
TODAY=$(date +%Y%m%d)

# Create the backup
cp "$SOURCE_FILE" "$BACKUP_DIR/mcp_$TODAY.json"

# Optional: Remove backups older than RETENTION_DAYS
find "$BACKUP_DIR" -name "mcp_*.json" -type f -mtime +$RETENTION_DAYS -delete

echo "Backup created: $BACKUP_DIR/mcp_$TODAY.json"
