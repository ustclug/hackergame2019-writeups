package main

import (
	"WonderfulAdventure/asset"
	"errors"
	"github.com/gorilla/sessions"
	"github.com/gorilla/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"runtime"
	"time"
)

const (
	Version         = "0.0.1"
	Author          = "ertuil"
	debug           = false
	debugHost       = "127.0.0.1:8080"
	debugSessionKey = "adwaaabbbccc123fads90wn"
	leaseHost       = "[::]:80"
)

var (
	store    = sessions.NewCookieStore([]byte(debugSessionKey))
	upgrader = websocket.Upgrader{}
)

func IndexHandler(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "statics/html/index.html")
}

func WebSocketHandler(w http.ResponseWriter, r *http.Request) {

	c, _ := upgrader.Upgrade(w, r, nil)

	go CoreWsHandle(c)
}

func CoreWsHandle(c *websocket.Conn) {
	defer c.Close()

	se := state{}
	se.setState(0, 0, 100, "")
	se.count = 0
	var err error
	for {
		switch se.Stage {
		case 0:
			err = Stage0(c, &se)
		case 1:
			err = Stage1(c, &se)
		case 2:
			err = Stage2(c, &se)
		case 3:
			err = Stage3(c, &se)
		case 4:
			err = Stage4(c, &se)
		case 5:
			err = Stage5(c, &se)
		case 6:
			err = Stage6(c, &se)
		case 7:
			err = Stage7(c, &se)
		case 10:
			getFlag(c, &se)
		default:
			err = errors.New(errst)
		}
		// 破产
		if se.Money < 0 {
			j, _ := MsgInitJson("旁白", "你已经破产了！", []string{}, se)
			_ = c.WriteMessage(websocket.TextMessage, j)
			break
		}
		if err != nil {
			log.Println(err)
			j, _ := MsgInitJson("旁白", errst, []string{}, se)
			_ = c.WriteMessage(websocket.TextMessage, j)
			break
		}
		if se.Stage == failstate {
			break
		}
		time.Sleep(300 * time.Microsecond)
	}
}

func main() {
	// 多核运行
	runtime.GOMAXPROCS(runtime.NumCPU())

	// 释放静态资源
	if err := asset.RestoreAssets(".", "statics"); err != nil {
		log.Panic(err)
	}
	// 初始化状态转移矩阵
	stateTransInit()

	// 路由
	http.Handle("/statics/", http.StripPrefix("/statics/", http.FileServer(http.Dir("./statics"))))
	http.HandleFunc("/", IndexHandler)
	http.HandleFunc("/ws", WebSocketHandler)

	// 启动服务
	var host string
	if debug {
		host = debugHost
	} else {
		host = leaseHost
	}
	log.Println("Start listening to", host)
	err := http.ListenAndServe(host, nil) //设置监听的端口
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}

}

func getFlag(c *websocket.Conn, se *state) {
	var flag string
	var err error
	if debug {
		flag = readFlagDebug()
	} else {
		flag, err = readFlagFromFile("flag.txt")
		if err != nil {
			flag = "无法获取flag，请联系管理员。"
		}
	}

	j, _ := MsgInitJson("系统", flag, []string{}, *se)
	_ = c.WriteMessage(websocket.TextMessage, j)
	se.Stage = 11
}

func readFlagFromFile(filename string) (string, error) {
	b, err := ioutil.ReadFile("flag.txt")
	if err != nil {
		return "", err
	}
	return string(b), nil
}

func readFlagDebug() string {
	return "flag{haha_this_is_flag}"
}
