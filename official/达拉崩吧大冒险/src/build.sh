go-bindata -o=./asset/asset.go -pkg=asset statics/...
go build -o bin/wa-darwin WonderfulAdventure
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o bin/wa-linux WonderfulAdventure
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o bin/wa-windows.exe WonderfulAdventure
cp -f flag.txt bin/flag.txt