echo "=> Creating the admin user in MongoDB"
echo 'use admin
db.createUser( { user: "admin", pwd: "admin", roles: [ { role: "userAdminAnyDatabase", db: "admin"},"backup","restore"] } ) 
exit' | mongo -p admin --authenticationDatabase admin --host mongo.svc --port 27017

echo "=> Creating the mgi user in MongoDB"
echo 'use mgi
db.createUser( { user: "mgi_user", pwd: "mgi_password", roles: [ "readWrite" ] } ) 
exit '| mongo -p admin --authenticationDatabase admin --host mongo.svc --port 27017



