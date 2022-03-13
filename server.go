package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	handler := http.HandlerFunc(handleRequest)
	http.Handle("/image", handler)
	http.ListenAndServe(":4000", nil)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")

	way := "images/image" + id
	fmt.Println(way)
	fileBytes, err := ioutil.ReadFile(way)
	if err != nil {
		panic(err)
	}
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/octet-stream")
	w.Write(fileBytes)
	return
}
