
#!/bin/bash

CHANNEL_NAME="mychannel"
CHAINCODE_NAME="mycc"
CHAINCODE_VERSION="1.0"
CHAINCODE_PATH=./hyperledger-fabric-the-hard-way/chaincode
CHAINCODE_LANG="golang"
ORDERER_CA=./crypto-config/ordererOrganizations/bi.example.com/tlsca/tlsca.bi.example.com-cert.pem

# Fonction pour définir les variables d'environnement pour un peer
setPeerEnv() {
  PEER=$1
  ORG=$2

  if [ $ORG == "dana" ]; then
    CORE_PEER_LOCALMSPID="DanaMSP"
    CORE_PEER_TLS_ROOTCERT_FILE=./crypto-config/peerOrganizations/dana.example.com/tlsca/tlsca.dana.example.com-cert.pem
    CORE_PEER_MSPCONFIGPATH=./crypto-config/peerOrganizations/dana.example.com/users/Admin@dana.example.com/msp
    CORE_PEER_ADDRESS=$PEER.dana.example.com:7051
  elif [ $ORG == "gopay" ]; then
    CORE_PEER_LOCALMSPID="GopayMSP"
    CORE_PEER_TLS_ROOTCERT_FILE=./crypto-config/peerOrganizations/gopay.example.com/tlsca/tlsca.gopay.example.com-cert.pem
    CORE_PEER_MSPCONFIGPATH=./crypto-config/peerOrganizations/gopay.example.com/users/Admin@gopay.example.com/msp
    CORE_PEER_ADDRESS=$PEER.gopay.example.com:9051
  else
    echo "ORG inconnu"
    exit 1
  fi
}

# Création du canal
 peer channel create -o orderer0.bi.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/channel.Tx --tls --cafile $ORDERER_CA

# Installation de la chaincode sur les peers de Dana
for PEER in peer0 peer1; do
  setPeerEnv $PEER "dana"
  peer chaincode install -n $CHAINCODE_NAME -v $CHAINCODE_VERSION -p $CHAINCODE_PATH -l $CHAINCODE_LANG
done

# Installation de la chaincode sur les peers de Gopay
for PEER in peer0 peer1; do
  setPeerEnv $PEER "gopay"
  peer chaincode install -n $CHAINCODE_NAME -v $CHAINCODE_VERSION -p $CHAINCODE_PATH -l $CHAINCODE_LANG
done

# Instanciation de la chaincode sur le canal (peer0.dana)
  setPeerEnv peer0 "dana"
  peer chaincode instantiate -o orderer0.bi.example.com:7050 --tls --cafile $ORDERER_CA -C $CHANNEL_NAME -n $CHAINCODE_NAME -l $CHAINCODE_LANG -v $CHAINCODE_VERSION -c '{"Args":["init","a","100","b","200"]}' -P "OR ('DanaMSP.peer','GopayMSP.peer')"

# Interroger la chaincode sur peer0.dana.example.com
peer chaincode query -C $CHANNEL_NAME -n $CHAINCODE_NAME -c '{"Args":["query","a"]}'
