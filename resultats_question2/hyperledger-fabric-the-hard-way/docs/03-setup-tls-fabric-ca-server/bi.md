# Setup Hyperledger TLS CA
This CA generates the certificates used to secure communications on Transport Layer Security (TLS). For this reason, this CA is often referred to as a “TLS CA”. These TLS certificates are attached to actions as a way of preventing “man in the middle” attacks. 

### Setup Database
for the sake of simplicity, we will deploy database on docker

ssh to the nodes
```shell
vagrant ssh bi-ca-server-0
```

create directory for docker related files
```shell
mkdir -p docker-compose/tls/
cat <<EOF | tee docker-compose/tls/docker-compose.yaml
version: "2"
services:
  tls-fabric-bi-ca-postgres:
    ports:
      - "5432:5432"
    container_name: tls-fabric-bi-ca-postgres
    environment:
      POSTGRES_DB: tls_fabric_bi_ca
      POSTGRES_USER: tls-fabric-bi-ca-user
      POSTGRES_PASSWORD: tls-fabric-bi-ca-password
    image: postgres:12-alpine
    restart: always
    volumes:
      - tls-fabric-bi-ca-postgres:/var/lib/postgresql/data
volumes:
  tls-fabric-bi-ca-postgres:
    driver: local
EOF
sudo docker-compose --file docker-compose/tls/docker-compose.yaml up --build -d 
```

### Setup Fabric CA
create config directory
```shell
sudo mkdir -p /etc/hyperledger/tls-fabric-ca
```

create TLS fabric CA configuration
```shell
cat <<EOF | sudo tee /etc/hyperledger/tls-fabric-ca/fabric-ca-server-config.yaml
# Service definition for Hyperledger fabric-ca server

version: 1.5.2
port: 7054

cors:
    enabled: false
    origins:
      - "*"

debug: false
crlsizelimit: 512000

tls:
  enabled: true
  keyfile: /etc/secrets/bi/services/tls-fabric-ca-server/tls/key.pem
  certfile: /etc/secrets/bi/services/tls-fabric-ca-server/tls/cert.pem
  clientauth:
    type: NoClientCert

ca:
  name: intermediate.tls.bi.go.id
  keyfile: /etc/secrets/bi/tlsca/intermediate-key.pem
  certfile: /etc/secrets/bi/tlsca/intermediate-cert.pem
  chainfile: /etc/secrets/bi/tlsca/intermediate-bundle.pem
  reenrollIgnoreCertExpiry: false

crl:
  expiry: 24h

registry:
  maxenrollments: -1

  identities:
     - name: root@tls.bi.go.id
       pass: root-password
       type: client
       affiliation: ""
       attrs:
          hf.Registrar.Roles: "*"
          hf.Registrar.DelegateRoles: "*"
          hf.Revoker: true
          hf.IntermediateCA: true
          hf.GenCRL: true
          hf.Registrar.Attributes: "*"
          hf.AffiliationMgr: true

db:
  type: postgres
  datasource: host=localhost port=5432 user=tls-fabric-bi-ca-user password=tls-fabric-bi-ca-password dbname=tls_fabric_bi_ca sslmode=disable
  tls:
      enabled: false

ldap:
   enabled: false

affiliations:
   org1:
      - department1
      - department2
   org2:
      - department1

signing:
    default:
      usage:
        - digital signature
      expiry: 8760h
    profiles:
      ca:
         usage:
           - cert sign
           - crl sign
         expiry: 43800h
         caconstraint:
           isca: true
           maxpathlen: 0
      tls:
         usage:
            - signing
            - key encipherment
            - server auth
            - client auth
            - key agreement
         expiry: 8760h

csr:
   cn:
   keyrequest:
     algo: ecdsa
     size: 256
   names:
      - C: id
        ST: jakarta
        L:
        O: bi
        OU:
   hosts:
     - localhost
   ca:
      expiry: 131400h
      pathlength: 1

idemix:
  rhpoolsize: 1000
  nonceexpiration: 15s
  noncesweepinterval: 15m

bccsp:
    default: SW
    sw:
        hash: SHA2
        security: 256
        filekeystore:
            keystore: msp/keystore

cacount:
cafiles:

intermediate:
  parentserver:
    url:
    caname:

  enrollment:
    hosts:
    profile:
    label:

  tls:
    certfiles:
    client:
      certfile:
      keyfile:

cfg:
  identities:
    passwordattempts: 10

operations:
    listenAddress: 127.0.0.1:9443
    tls:
        enabled: false
        cert:
            file:
        key:
            file:
        clientAuthRequired: false
        clientRootCAs:
            files: []

metrics:
    provider: prometheus
EOF
```

create tls-fabric-ca-server.service systemd unit file
```shell
cat <<EOF | sudo tee /etc/systemd/system/tls-fabric-ca-server.service
# Service definition for Hyperledger fabric-ca server
[Unit]
Description=hyperledger tls fabric-ca server - Certificate Authority for TLS hyperledger fabric
Documentation=https://hyperledger-fabric-ca.readthedocs.io/
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
Restart=on-failure
Environment=FABRIC_CA_HOME=/etc/hyperledger/tls-fabric-ca
Environment=FABRIC_CA_SERVER_HOME=/etc/hyperledger/tls-fabric-ca
Environment=CA_CFG_PATH=/etc/hyperledger/tls-fabric-ca
ExecStart=/usr/local/bin/fabric-ca-server start

[Install]
WantedBy=multi-user.target
EOF
```

start TLS fabric CA server
```shell
sudo systemctl enable tls-fabric-ca-server.service
sudo systemctl start tls-fabric-ca-server.service
sudo systemctl status tls-fabric-ca-server.service
```

### Enrolling Admin Users
By default, TLS Fabric CA will create an root identity
```
- name: root@tls.bi.go.id
  pass: root-password
```
This root identity is used for creating another identity for admin, client, and orderer nodes. In order to create another identity, we need to first collect the certificate from this root identity

create directory for root identity
```
mkdir -p organizations/OrdererOrganizations/bi/users/root@tls.bi.go.id/tls
```

get root identity certificate
```
fabric-ca-client enroll -d -u https://root@tls.bi.go.id:root-password@10.250.250.10:7054 --tls.certfiles ${HOME}/organizations/OrdererOrganizations/bi/msp/tlsintermediatecerts/intermediate-cert.pem --enrollment.profile tls --csr.hosts 'root' --csr.names C=id,O=bi,ST=jakarta --mspdir ${HOME}/organizations/OrdererOrganizations/bi/users/root@tls.bi.go.id/tls
```

if we check, we will find
```
tree organizations
organizations
└── OrdererOrganizations
    └── bi
        ├── msp
        │   ├── cacerts
        │   │   └── root-cert.pem
        │   ├── intermediatecerts
        │   │   └── intermediate-cert.pem
        │   ├── tlscacerts
        │   │   └── root-cert.pem
        │   └── tlsintermediatecerts
        │       └── intermediate-cert.pem
        └── users
            └── root@tls.bi.go.id
                └── tls
                    ├── IssuerPublicKey
                    ├── IssuerRevocationPublicKey
                    ├── cacerts
                    ├── keystore
                    │   └── 8730d406f1662b8292e1fb76c4cd0a1ad8d2fbb10aeb10aa0de2c466d0883cc3_sk
                    ├── signcerts
                    │   └── cert.pem
                    ├── tlscacerts
                    │   └── tls-10-250-250-10-7054.pem
                    ├── tlsintermediatecerts
                    │   └── tls-10-250-250-10-7054.pem
                    └── user
```

### Creating Identity
now, let's use this to register another identity for orderer. We will using this when creating orderer service
```
fabric-ca-client register -d --id.name orderer0@tls.bi.go.id --id.secret orderer0-password -u https://10.250.250.10:7054  --id.type client --tls.certfiles ${HOME}/organizations/OrdererOrganizations/bi/msp/tlsintermediatecerts/intermediate-cert.pem --mspdir ${HOME}/organizations/OrdererOrganizations/bi/users/root@tls.bi.go.id/tls
fabric-ca-client register -d --id.name orderer1@tls.bi.go.id --id.secret orderer1-password -u https://10.250.250.10:7054  --id.type client --tls.certfiles ${HOME}/organizations/OrdererOrganizations/bi/msp/tlsintermediatecerts/intermediate-cert.pem --mspdir ${HOME}/organizations/OrdererOrganizations/bi/users/root@tls.bi.go.id/tls
fabric-ca-client register -d --id.name orderer2@tls.bi.go.id --id.secret orderer2-password -u https://10.250.250.10:7054  --id.type client --tls.certfiles ${HOME}/organizations/OrdererOrganizations/bi/msp/tlsintermediatecerts/intermediate-cert.pem --mspdir ${HOME}/organizations/OrdererOrganizations/bi/users/root@tls.bi.go.id/tls
```
