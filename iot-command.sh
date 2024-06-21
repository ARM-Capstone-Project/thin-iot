
aws iot describe-endpoint --endpoint-type IoT:Data-ATS

aws iot describe-endpoint --endpoint-type iot:CredentialProvider

sudo /greengrass/v2/bin/greengrass-cli component list

sudo /greengrass/v2/bin/greengrass-cli deployment create \
    --recipeDir ~/alco/components/recipe \
    --artifactDir ~/alco/components/artifacts \
    --merge "com.alco.dh22=1.0.0"
Local deployment submitted! Deployment Id: e4054641-3c08-4691-a4ce-eb98c76f2620
#remove the component
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove "com.alco.dh22"
Local deployment submitted! Deployment Id: d1eea524-3321-404d-80f3-b21d4f19fdbd


python3 moistureSensor.py --endpoint your-endpoint \
--rootCA ~/certs/AmazonRootCA1.pem --cert ~/certs/raspberrypi-certificate.pem.crt \
--key ~/certs/raspberrypi-private.pem.key --thingName RaspberryPi --clientId RaspberryPi

sudo tail -f /greengrass/v2/logs/greengrass.log

java -jar ./GreengrassCore/lib/Greengrass.jar --version

cd ~/certificates
mv AmazonRootCA1.pem rootCA.pem
mv *-certificate.pem.crt certificate.pem
mv *-private.pem.key privateKey.pem
mv *-public.pem.key publicKey.pem
sudo mkdir -p /greengrass/v2/certificates
sudo chmod 755 /greengrass
cd ~/environment
sudo cp -avr certificates /greengrass/v2

#Greengrass

curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip
unzip greengrass-nucleus-latest.zip -d GreengrassCore && rm greengrass-nucleus-latest.zip

curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip && unzip greengrass-nucleus-latest.zip -d GreengrassInstaller


java -jar ./GreengrassCore/lib/Greengrass.jar --version


sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar --init-config ./GreengrassCore/config.yaml --component-default-user ggc_user:ggc_group --setup-system-service true

sudo tail -f /greengrass/v2/logs/greengrass.log

sudo service greengrass status -l

 {
    "Effect": "Allow",
    "Action": "iot:AssumeRoleWithCertificate",
    "Resource": "arn:aws:iot:ap-southeast-1:654654435122:rolealias/GreengrassV2TokenExchangeRoleAlias"
  }

aws greengrassv2 create-deployment --cli-input-json file://deployment.json
{
    "deploymentId": "1c6f968d-e198-48df-8fe1-52b1addf764c"
}  