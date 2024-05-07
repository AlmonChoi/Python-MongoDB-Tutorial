#!/usr/bin/env bash

#
# Backup Mongo database in Docker 
#

time_stamp=`date +%Y%m%d%H%M%S`
container_backup_path="/data/mongo_backup/backup/"


# Get parameters for MongoDB
function get_params(){
python3 <<EOF
import os
conf_file = "./config/settings.json"
setting_file = open(conf_file, "rt")
config_value = json.loads(setting_file.read())
print(config_value["APP_CONFIG_MONGODB_URL"], config_value["APP_CONFIG_MONGODB_NAME"]
EOF
}

# Get docker IP
function check_ip() {
    db_ip=$(docker inspect -f '{{ .NetworkSettings.Networks.db_net.IPAddress}}' mongo)
    if [[ $db_ip == "<no value>" ]]; then
        db_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}} {{.IPAddress}}{{end}}' mongo |awk '{print $1}')
    fi
    echo "$db_ip"
}

db_args=$(get_params)
db_host=$(check_ip)
db_port=$(echo $db_args |awk '{print $2}')
db_user=$(echo $db_args |awk '{print $3}')
db_password=$(echo $db_args |awk '{print $4}')
db_name=$(echo $db_args |awk '{print $5}'

docker exec mongo \
	mongodump --host $db_host --port $db_port -u $db_user -p $db_password \
        --gzip --authenticationDatabase $db_name -d $db_name \
        -o $container_backup_path$time_stamp


