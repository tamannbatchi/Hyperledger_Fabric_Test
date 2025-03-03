package main

import (
    "encoding/json"
    "fmt"
    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing an asset
type SmartContract struct {
    contractapi.Contract
}

// Asset represents an asset with an ID and value
type Asset struct {
    ID    string `json:"id"`
    Value string `json:"value"`
}

// InitLedger adds a base set of assets to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
    assets := []Asset{
        {ID: "asset1", Value: "value1"},
        {ID: "asset2", Value: "value2"},
    }

    for _, asset := range assets {
        assetJSON, err := json.Marshal(asset)
        if err != nil {
            return err
        }

        err = ctx.GetStub().PutState(asset.ID, assetJSON)
        if err != nil {
            return fmt.Errorf("failed to put asset: %v", err)
        }
    }

    return nil
}

// CreateAsset adds a new asset to the ledger
func (s *SmartContract) CreateAsset(ctx contractapi.TransactionContextInterface, id string, value string) error {
    asset := Asset{
        ID:    id,
        Value: value,
    }
    assetJSON, err := json.Marshal(asset)
    if err != nil {
        return err
    }

    return ctx.GetStub().PutState(id, assetJSON)
}

// ReadAsset retrieves an asset from the ledger
func (s *SmartContract) ReadAsset(ctx contractapi.TransactionContextInterface, id string) (*Asset, error) {
    assetJSON, err := ctx.GetStub().GetState(id)
    if err != nil {
        return nil, fmt.Errorf("failed to read asset: %v", err)
    }
    if assetJSON == nil {
        return nil, fmt.Errorf("asset %s does not exist", id)
    }

    var asset Asset
    err = json.Unmarshal(assetJSON, &asset)
    if err != nil {
        return nil, err
    }

    return &asset, nil
}

func main() {
    chaincode, err := contractapi.NewChaincode(new(SmartContract))
    if err != nil {
        fmt.Printf("Error create chaincode: %s", err.Error())
        return
    }

    if err := chaincode.Start(); err != nil {
        fmt.Printf("Error starting chaincode: %s", err.Error())
    }
}
