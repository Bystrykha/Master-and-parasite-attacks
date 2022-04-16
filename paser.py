package main

import (
	"fmt"
	_ "github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"io/ioutil"
	"net/http"
)

func main() {
	handler1 := http.HandlerFunc(sendJPG1G)
	handler2 := http.HandlerFunc(sendJPG500M)
	handler3 := http.HandlerFunc(injection)

	http.Handle("/image", handler1)
	http.Handle("/image2", handler2)
	http.Handle("/page", handler3)
	//http.ListenAndServe(":4000", nil)
	ip := &layers.IPv4{}
	for k := range ip{
		fmt.Println(k)
	}

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

func sendJPG500M(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	way := "images min 2/image (" + id + ")"
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

func injection(w http.ResponseWriter, r *http.Request) {
	fileBytes, err := ioutil.ReadFile("cachePacket.html")
	if err != nil {
		panic(err)
	}
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "text/html; charset=UTF-8")
	w.Write(fileBytes)
	return
}
