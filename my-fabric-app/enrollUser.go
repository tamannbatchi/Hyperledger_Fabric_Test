package main

import (
    "fmt"
    "github.com/hyperledger/fabric-sdk-go/pkg/client/msp"
    "github.com/hyperledger/fabric-sdk-go/pkg/core/config"
    "github.com/hyperledger/fabric-sdk-go/pkg/fabsdk"
    "log"
)

func main() {
    configPath := "./gateway/connection-org1.yaml"

    sdk, err := fabsdk.New(config.FromFile(configPath))
    if err != nil {
        log.Fatalf("Failed to create new SDK: %s\n", err)
    }
    defer sdk.Close()

    caClient, err := msp.New(sdk.Context(), msp.WithOrg("Dana"))
    if err != nil {
        log.Fatalf("Failed to create CA client: %s\n", err)
    }

    // Enroll the admin user
    err = caClient.Enroll("admin", msp.WithSecret("adminpw"))
    if err != nil {
        log.Fatalf("Failed to enroll admin user: %s\n", err)
    }

    fmt.Println("Successfully enrolled admin user")
}
