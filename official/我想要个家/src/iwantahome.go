package main

import (
	"bufio"
	"crypto/aes"
	"crypto/cipher"
	"encoding/hex"
	"errors"
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"os/exec"
	"runtime"
	"strings"
	"time"
)

const (
	ONESECOND = 1000000000
)

var (
	WantDir     = []string{"/Kitchen", "/Lavatory", "/Bedroom", "/Living_Room"}
	DontWantDir = []string{"/home", "/root", "/boot","/proc","/sys", "/etc","/bin"}
	PhoneFiles  = []string{"/Bedroom/Microphone", "/Bedroom/Headset"}
	ClockFiles  = []string{"/Living_Room/Clock"}
	key         = []byte{0xF7, 0x9D, 0x9B, 0x80, 0xA2, 0xC8, 0xA1, 0x75, 0x4C, 0x47, 0xA6, 0x54, 0x01, 0xFF, 0x6C, 0xFE}
	iv          = []byte{0x42, 0x8F, 0x0B, 0x63, 0xAD, 0xDC, 0x47, 0x40, 0xB5, 0x8C, 0x2A, 0xE5, 0xBC, 0x2F, 0x11, 0xCB}
)

func main() {
	fmt.Println("警告，做这道题的时候，如果方法不对，可能对操作系统造成严重危害。请在执行任何操作之前务必理解该操作所代表的含义。")
	fmt.Println("I just want a home. Please do what I say and I will give you a flag")
	fmt.Println("Make sure I am running on Linux(Unix).")
	// Check windows
	if runtime.GOOS == "windows" {
		fmt.Println("I am on Windows")
		os.Exit(1)
	}

	// Challenge 1 ---- rooms
	time.Sleep(ONESECOND)
	fmt.Println("I want these directories in / :", WantDir)
	time.Sleep(ONESECOND)

	err := CheckWantDir(WantDir)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println("Thanks, I find these directories.")

	time.Sleep(ONESECOND)
	fmt.Println("I hate these directories ", DontWantDir, ", Please delete them all!")
	time.Sleep(ONESECOND)

	err = CheckDontWantDir(DontWantDir)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println("Well done.")

	// Challenge 2 ---- telephone
	time.Sleep(ONESECOND)
	fmt.Println("Now I want a telephone in Bedroom")
	fmt.Println("I will write something to /Bedroom/Microphone and read the same thing in /Bedroom/Headset")
	time.Sleep(ONESECOND)
	err = CheckThingsExist(PhoneFiles)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	err = CheckPhonesFunc()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println("Good, telephone works well.")

	// Challenge 3 ---- clock

	time.Sleep(ONESECOND)
	fmt.Println("Time is important, I need a clock in living_room")
	fmt.Println("I will read  Beijing time (eg: '20:15:30') in /Living_Room/Clock")
	time.Sleep(ONESECOND)

	err = CheckThingsExist(ClockFiles)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	err = CheckClockFunc()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println("Good, the clock works well.")

	// Challenge 4 ---- sleep

	time.Sleep(ONESECOND)
	fmt.Println("It is late, tell me how to sleep 10 seconds in shell")
	time.Sleep(ONESECOND)

	err = CheckSleep()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	//EncryptFlag()
	err = GetFlag()
	if err != nil {
		fmt.Println(err)
	}

	runtime.GC()

}

// room functions
func CheckWantDir(wd []string) (err error) {
	for _, w := range wd {
		ret := CheckDict(w)
		if ret != true {
			return errors.New(fmt.Sprintf("Oh I can not find %v ,goodbye.", w))
		}
	}
	return nil
}

func CheckDontWantDir(wd []string) (err error) {
	for _, w := range wd {
		ret := CheckDict(w)
		if ret == true {
			return errors.New(fmt.Sprintf("Oh I found %v ,goodbye.", w))
		}
	}
	return nil
}

func CheckExist(path string) (ret bool) {
	// 检查文件是否存在
	_, err := os.Stat(path)
	if err != nil {
		if os.IsExist(err) {
			return true
		}
		return false
	}
	return true
}

func CheckDict(path string) (ret bool) {
	// 检查文件夹是否存在
	s, err := os.Stat(path)
	if err != nil {
		return false
	}
	return s.IsDir()
}

func ListDict(path string) (ret []string, err error) {
	dir, err := ioutil.ReadDir(path)
	if err != nil {
		return nil, err
	}

	ret = []string{}

	for _, d := range dir {
		ret = append(ret, d.Name())
	}
	return ret, nil
}

// Flag functions
func GetFlag() error {

	flagerr := errors.New("解密密码请联系管理员。")

	cmsg, err := hex.DecodeString("8f782f72626f78cf8d1efda9ab55a3ab91dbe0e4")
	if err != nil {
		fmt.Print(cmsg)
		return flagerr
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		fmt.Println(err)
		return err
	}

	ans := make([]byte, len(cmsg))

	decrypter := cipher.NewCFBDecrypter(block, iv)
	decrypter.XORKeyStream(ans, cmsg)
	fmt.Println(string(ans))
	fmt.Println("如果您使用逆向工程的方式解出了此题，首先恭喜你获得了 flag，在赛后我们会公布writeup，别忘了来看我们的预期解")
	return  nil
}

//func EncryptFlag() {
//	msg := []byte("flag{I_am_happy_now}")
//	err := errors.New("解密密码请联系管理员。")
//
//	block, err := aes.NewCipher(key)
//	if err != nil {
//		fmt.Println(err)
//	}
//
//	cmsg := make([]byte, len(msg))
//
//	encrypter := cipher.NewCFBEncrypter(block,iv)
//	encrypter.XORKeyStream(cmsg, msg)
//	fmt.Println(hex.EncodeToString(cmsg))
//}

// Phone functions
func CheckThingsExist(wd []string) error {
	for _, w := range wd {
		ret := CheckExist(w)
		if !ret {
			return errors.New(fmt.Sprintln("I can not find ", w, " in Bedroom"))
		}
	}
	return nil
}

func CheckPhonesFunc() error {
	msg := RandomString()

	err := ioutil.WriteFile(PhoneFiles[0], []byte(msg), 0644)
	if err != nil {
		return errors.New("phone error: can not write to /Bedroom/Microphone")
	}

	b, err := ioutil.ReadFile(PhoneFiles[1])
	if err != nil {
		return errors.New("phone error: can not read from /Bedroom/Headset")
	}
	if string(b) != msg {
		return errors.New(fmt.Sprintf("Write %v but read %v", msg, b))
	}
	return nil
}

func RandomString() string {
	rand.Seed(time.Now().UnixNano())
	letterRunes := []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

	b := make([]rune, 16)
	for i := range b {
		b[i] = letterRunes[rand.Intn(len(letterRunes))]
	}
	return string(b)
}

// Clock functions

func CheckClockFunc() error {

	// 设置正确时间
	var cstSh = time.FixedZone("CST", 8*3600)
	hour, min, sec := time.Now().In(cstSh).Clock()
	formatTimeStr := fmt.Sprintf("%02d:%02d:%02d", hour, min, sec)

	// 读取时间
	read, err := ioutil.ReadFile(ClockFiles[0])
	if err != nil {
		return errors.New("I can not read the clock")
	}
	sread := string(read)

	// 去除空格换行
	sread = strings.Replace(sread, " ", "", -1)
	sread = strings.Replace(sread, "\n", "", -1)

	if sread != formatTimeStr {
		return errors.New(fmt.Sprintf("Time is not correct, it shound be '%v' not '%v'", formatTimeStr, sread))
	}
	return nil
}

// Sleep function

func CheckSleep() error {

	inputReader := bufio.NewReader(os.Stdin)
	fmt.Print("> ")
	input, err := inputReader.ReadString('\n')
	if err != nil {
		return errors.New("I can not read input")
	}

	// 删除换行符号
	input = strings.Replace(input,"\n","",-1)
	fmt.Printf("command is:'%v'\n",input)

	inputs := strings.Split(input," ")
	t1 := time.Now()

	var cmd *exec.Cmd
	if len(inputs) < 0 {
		return errors.New("empty command")
	} else if len(inputs) == 1 {
		cmd = exec.Command(inputs[0])
	} else {
		cmd = exec.Command(inputs[0],inputs[1:]...)
	}
	err = cmd.Run()
	if err != nil {
		return errors.New(fmt.Sprintf("Command error:%v",err))
	}
	ts := time.Since(t1)

	fmt.Println("I slept for ",ts)
	if ts < 10000000000 {
		return errors.New("I need to sleep longer")
	}
	return nil
}