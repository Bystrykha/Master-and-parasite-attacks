for (let i = 0; i < 1000; ++i){
    const n = new Image();
    n.src = "http://localhost:4000/image?id=" + i.toString();
}
