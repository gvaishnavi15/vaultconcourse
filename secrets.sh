#!/bin/bash

# selecting authentication method as userpass by default it is token
vault login -method=userpass username=vaishnavi password=vaishnavi

# retrieving secrets from the vault
username=$(vault kv get -field=username mysecrets/path)
password=$(vault kv get -field=password mysecrets/path)

# reading and printing userpass
echo "Retrived Username: $username"
echo "Retrived Password: $password"