#!/bin/bash
#Create CA
csmanage ca create --dir ../security/ SJ
#Create runtime ELX
csmanage runtime create --dir ../security SJ --attr-file runtime_attributes/ELX.json
#Export CA cert into runtime truststore (common for all runtimes)
csmanage ca export --dir ../security SJ ../security/runtimes/truststore_for_transport/
#Create runtime Lund_RFID
csmanage runtime create --dir ../security/ SJ --attr-file ../runtime_attributes/Lund_RFID.json
#Create runtime Lund_Camera_Sensehat
csmanage runtime create --dir ../security/ SJ --attr-file ../runtime_attributes/Lund_Camera_Sensehat.json 
#Create runtime Lund_InfoBoard
csmanage runtime create --dir ../security/ SJ --attr-file ../runtime_attributes/Lund_InfoBoard.json 
#Create runtime Sthlm_RFID
csmanage runtime create --dir ../security/ SJ --attr-file ../runtime_attributes/Sthlm_RFID.json
#Create runtime Sthlm_Camera_Sensehat
csmanage runtime create --dir ../security/ SJ --attr-file ../runtime_attributes/Sthlm_Camera_Sensehat.json 
#Create runtime Sthlm_InfoBoard
csmanage runtime create --dir ../security/ SJ --attr-file ../runtime_attributes/Sthlm_InfoBoard.json 


csmanage ca signCSR --dir ../security/ SJ ../security/runtimes/SJ++++ELX/SJ++++ELX.csr
csmanage ca signCSR --dir ../security/ SJ ../security/runtimes/SJ++++Lund_Camera_Sensehat/SJ++++Lund_Camera_Sensehat.csr
csmanage ca signCSR --dir ../security/ SJ ../security/runtimes/SJ++++Lund_RFID/SJ++++Lund_RFID.csr
csmanage ca signCSR --dir ../security/ SJ ../security/runtimes/SJ++++Lund_InfoBoard/SJ++++Lund_InfoBoard.csr
csmanage ca signCSR --dir ../security/ SJ ../security/runtimes/SJ++++Sthlm_Camera_Sensehat/SJ++++Sthlm_Camera_Sensehat.csr
csmanage ca signCSR --dir ../security/ SJ ../security/runtimes/SJ++++Sthlm_RFID/SJ++++Sthlm_RFID.csr
csmanage ca signCSR --dir ../security/ SJ ../security/runtimes/SJ++++Sthlm_InfoBoard/SJ++++Sthlm_InfoBoard.csr
csmanage import --dir ../security ../security/SJ/newcerts/*

