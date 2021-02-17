import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pprint import pprint
from netmiko import ConnectHandler
import pandas
from shutil import copyfile
import logging
from datetime import date
from datetime import datetime
import time


## Format Todays Date ###
todaydate = date.today().strftime("%Y-%m-%d")
#todaydate = '2020-09-21'
todaydatelog = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
## Logging Module
logging.basicConfig(filename='app-'+todaydate+'.log', filemode='a', format=todaydatelog+" "+'%(levelname)s - %(message)s',level=logging.DEBUG)

try:
############################# Parse CSV File #####################################
    df = pandas.read_csv('wxc_script_config.csv')
    WxC_Username = df['WxC_Username'][0]
    WxC_Password = df['WxC_Password'][0]
    WxC_RegistrarDomain = df['WxC_RegistrarDomain'][0]
    WxC_OutboundProxyAddress = df['WxC_OutboundProxyAddress'][0]
    WxC_LinePort = df['WxC_LinePort'][0]
    WxC_SourceInterfaceName = df['WxC_SourceInterfaceName'][0]
    WxC_SourceInterfaceIP = df['WxC_SourceInterfaceIP'][0]
    WxC_ExtensionsRange = df['WxC_ExtensionsRange'][0]
    WxC_PSTNIP = df['WxC_PSTNIP'][0]
    Company_DomainName = df['Company_DomainName'][0]
    cfg_template = df['cfg_template'][0]
    CUBE_IP = df['CUBE_IP'][0]
    CUBE_Username = df['CUBE_Username'][0]
    CUBE_Password = df['CUBE_Password'][0]
    CUBE_SaveConfig = df['CUBE_SaveConfig'][0]
    logging.debug('## Parameters has been imported successfully')
    print(todaydatelog+ "-- Parameters has been imported successfully")
####################################################################################
############################# Import Configuration Template ########################
    cfg_template = open(cfg_template,"r")
    cfg_cube_config = cfg_template.read()
    cfg_template.close
    logging.debug('## Configuration template has been successfully imported')
    print(todaydatelog+ "-- Configuration template has been successfully imported")
#####################################################################################
############################# Prepare WxC CUBE Configuration ########################
    WxC_ExtensionsRange = WxC_ExtensionsRange.replace("X",".")
    cfg_cube_config = cfg_cube_config.replace("WxC_Username",WxC_Username)
    cfg_cube_config = cfg_cube_config.replace("WxC_Password",WxC_Password)
    cfg_cube_config = cfg_cube_config.replace("WxC_RegistrarDomain",WxC_RegistrarDomain)
    cfg_cube_config = cfg_cube_config.replace("WxC_OutboundProxyAddress",WxC_OutboundProxyAddress)
    cfg_cube_config = cfg_cube_config.replace("WxC_LinePort",WxC_LinePort)
    cfg_cube_config = cfg_cube_config.replace("WxC_SourceInterfaceName",WxC_SourceInterfaceName)
    cfg_cube_config = cfg_cube_config.replace("WxC_SourceInterfaceIP",WxC_SourceInterfaceIP)
    cfg_cube_config = cfg_cube_config.replace("WxC_PSTNIP",WxC_PSTNIP)
    cfg_cube_config = cfg_cube_config.replace("Company_DomainName",Company_DomainName)
    cfg_cube_config = cfg_cube_config.replace("WxC_ExtensionsRange",WxC_ExtensionsRange)
    f = open("cfg_cube_config_temp.txt","w")
    f.write(cfg_cube_config)
    f = open("cfg_cube_config_temp.txt","r")
    copyfile("cfg_cube_config_temp.txt","cfg_cube_config.txt")
    logging.debug('## Configuration file has been created cfg_cube_config.txt')
    print(todaydatelog+ "-- Configuration file has been created cfg_cube_config.txt")
#####################################################################################
############################# Connect to Cisco CUBE #################################
    router = {"device_type": "cisco_ios","host": CUBE_IP, "user": CUBE_Username, "pass":CUBE_Password}
    logging.debug('## Connecting to Cisco IOS Router')
    print(todaydatelog+ "-- Please wait while connecting to Cisco IOS Router")
    net_connect = ConnectHandler(ip=router["host"],username=router["user"],password=router["pass"],device_type=router["device_type"])
    output = net_connect.send_config_from_file("cfg_cube_config.txt")
    if CUBE_SaveConfig == 'YES':
        output += net_connect.save_config()
    logging.debug('## Configuration file has been sent to the router')
    print(todaydatelog+ "-- Configuration file has been sent to the router")
    print(todaydatelog+ "-- Please wait 2-3 minutes untill the trunk is registered")
    time.sleep(150) # Sleep for 3 seconds
##########################################################################################
############################# Check Registeration Status #################################
    send_cli = net_connect.send_command("show sip-ua register status")
    send_cli = send_cli.split()
    regiter_status = send_cli[send_cli.index(WxC_LinePort)+3]
    print(regiter_status)
    if regiter_status == 'no':
        print(todaydatelog+ "-- The WebEx Calling trunk has failed to register please check your WxC SIP trunk credentials, DNS or IP network configuration")
        logging.debug('Your WebEx Calling Trunk has not reistered please check your WxC SIP trunk credentials, DNS or IP network configuration')
    else:
        print(todaydatelog+ "-- The WebEx Calling Trunk has successfully registered")
    logging.debug('Your WebEx Calling Trunk has successfully registered')
except Exception as err:
    print(err)
    logging.error(err)
