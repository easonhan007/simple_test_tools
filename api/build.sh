env GOOS=linux go build -o server_linux server.go 
go build -o server_mac server.go 
env GOOS=windows go build -o server_win.exe server.go 
