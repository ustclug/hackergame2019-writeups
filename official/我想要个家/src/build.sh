CGO_ENABLED=0 GOOS=darwin go build -o bin/IWantAHome-darwin -ldflags "-w -s"
CGO_ENABLED=0 GOOS=linux go build -o bin/IWantAHome-linux -ldflags "-w -s"

