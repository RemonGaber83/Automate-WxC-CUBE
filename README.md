# WxC-CUBE-Config
Automate WxC CUBE Configuration
This script is used to automate WxC CUBE Configuration
config_template.txt is the configuration template used and it includes the SIP configuration the SIP provider. It might be changed for different providers configuration.
After creating the location and the gateway in WebEx Control Hub you will need to copy the SIP trunk parameters to the wxc_script_config.csv CSV file.
Define the internal number range in the CSV file.
Define the CUBE IP address and credentials.
Once you run the script it will generate the configuration send it to the router.
You will need to wait 3 minutes until the SIP trunk register.
By default the script doesn’t save the configuration however you can uncomment “#ouput += net_connect.save_config()” to save the config
Version 1.0 only allows WxC extension ranges to be subset of the DID Range for example the DID range should be +613941373XX and WxC range should be 73XX
