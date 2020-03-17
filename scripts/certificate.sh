#./certificate.sh <certificatepath>
host=`hostname --fqdn`
echo $host
mkdir -p $1
if [[ -f "$1/keystore.jks" ]];then
	rm -rf $1/keystore.jks
fi
keytool -genkey -alias jdaconnect -keypass changeme -keyalg RSA -keystore $1/keystore.jks -storetype jks -storepass changeme -keysize 2048 -dname "CN=${host}, OU=JDA Connect, O=JDA Software, L=Bangalore ST=KA, C=IN" -validity 365
if [[ -f "$1/${host}.cer" ]];then
	rm -rf $1/${host}.cer
fi
keytool  -export -alias jdaconnect  -file $1/${host}.cer -keystore $1/keystore.jks -storepass changeme
if [[ -f "$1/truststore.jks" ]];then
	rm -rf $1/truststore.jks
fi
keytool -import -v -trustcacerts -alias jdaconnect  -file $1/${host}.cer -keystore $1/truststore.jks -storepass changeme -noprompt