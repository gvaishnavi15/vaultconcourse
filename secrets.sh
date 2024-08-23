#!/bin/bash

# selecting authentication method as userpass by default it is token
export VAULT_ADDR='http://192.168.3.54:8200'
export VAULT_TOKEN=hvs.XMsDxvmQhWHMbDpfhxbA2ZlQ
# vault login -method=userpass username=vaishnavi password=vaishnavi

# retrieving secrets from the vault
username=$(vault kv get -field=username mysecrets/path)
password=$(vault kv get -field=password mysecrets/path)

screener_username=$(vault kv get -field=username screener/path)
screener_password=$(vault kv get -field=password screener/path)

# reading and printing userpass
echo "Retrived Username: $username"
echo "Retrived Password: $password"
echo "Retrived Screener Username: $screener_username"
echo "Retrived Screener Password: $screener_password"