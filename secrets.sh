export VAULT_ADDR='http://192.168.3.54:8200'
export VAULT_TOKEN='test'

EMAIL=$(vault kv get -field=userid screener/path)
PASSWORD=$(vault kv get -field=password screener/path)
PG_USER=$(vault kv get -field=PG_USER screener/path)
PG_PASS=$(vault kv get -field=PG_PASS screener/path)
PG_DB=$(vault kv get -field=PG_DB screener/path)

mkdir -p credentials
chmod +x credentials
echo "$EMAIL" > credentials/email.txt
echo "$PASSWORD" > credentials/password.txt
echo "$PG_USER" > credentials/pg_user.txt
echo "$PG_PASS" > credentials/pg_pass.txt
echo "$PG_DB" > credentials/pg_db.txt

# Print the credentials for debugging (ensure this is secure and not used in production)
echo "Fetched Email: $EMAIL"
echo "Fetched Password: $PASSWORD"
echo "Fetched PG_USER: $PG_USER"
echo "Fetched PG_PASS: $PG_PASS"
echo "Fetched PG_DB: $PG_DB"

ls -l credentials
