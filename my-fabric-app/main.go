package main

import (
    "fmt"
    "github.com/hyperledger/fabric-sdk-go/pkg/gateway"
    "log"
)

func main() {
    // Chargement d'un portefeuille contenant des identités pour accéder au réseau
    wallet, err := gateway.NewFileSystemWallet("wallet")
    if err != nil {
        log.Fatalf("Failed to create wallet: %s\n", err)
    }

    if !wallet.Exists("appUser") {
        fmt.Println("An identity for the user \"appUser\" does not exist in the wallet")
        fmt.Println("Run the enrollUser.go program before retrying")
        return
    }

    // Connection au gateway peer
    gw, err := gateway.Connect(
        gateway.WithConfig(gateway.ConfigOption{ConfigFile: "./gateway/connection-org1.yaml"}),
        gateway.WithIdentity(wallet, "appUser"),
    )
    if err != nil {
        log.Fatalf("Failed to connect to gateway: %s\n", err)
    }
    defer gw.Close()

    network, err := gw.GetNetwork("mychannel")
    if err != nil {
        log.Fatalf("Failed to get network: %s\n", err)
    }

    contract := network.GetContract("mychaincode")

    // Soumission des transactions
    result, err := contract.SubmitTransaction("CreateAsset", "asset1", "value1")
    if err != nil {
        log.Fatalf("Failed to submit transaction: %s\n", err)
    }
    fmt.Printf("Result: %s\n", result)

    result, err = contract.EvaluateTransaction("ReadAsset", "asset1")
    if err != nil {
        log.Fatalf("Failed to evaluate transaction: %s\n", err)
    }
    fmt.Printf("Result: %s\n", result)
}
