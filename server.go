package main

import (
	"fmt"
	_ "github.com/google/gopacket"
	"io/ioutil"
	"net/http"
)

func main() {
	handler1 := http.HandlerFunc(sendJPG1G)
	http.Handle("/image", handler1)

	http.ListenAndServe(":4000", nil)
}

func sendJPG1G(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	way := "images min/image (" + id + ")"
	fmt.Println(way)
	fileBytes, err := ioutil.ReadFile(way)
	if err != nil {
		panic(err)
	}
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Cache-Control", "public, max-age=31536000")
	w.Header().Set("Content-Type", "application/octet-stream")
	w.Write(fileBytes)
	return
}
