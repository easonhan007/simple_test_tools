package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type User struct {
	Name   string
	Age    int
	Sex    string
	Job    string
	Mobile string
}

type Pong struct {
	Status  int
	Message string
}

func main() {
	http.HandleFunc("/user", user)
	http.HandleFunc("/ping", pong)
	fmt.Println("Server start at localhost:3000")
	http.ListenAndServe(":3000", nil)
}

func user(w http.ResponseWriter, r *http.Request) {
	fmt.Println("/api")
	user := User{"Alex", 20, "Male", "Programmer", "18888888888"}

	js, err := json.Marshal(user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(js)
}

func pong(w http.ResponseWriter, r *http.Request) {
	fmt.Println("/api")
	pong := Pong{200, "pong"}

	js, err := json.Marshal(pong)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(js)
}
