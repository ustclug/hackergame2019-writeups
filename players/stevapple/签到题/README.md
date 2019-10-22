# 签到题（iPadOS/iOS）

查看页面源码获得提示，判断出需要删除 disabled 属性；通过 Safari 向网页中注入如下 Javascript：

```Javascript
document.getElementsByTagName('button')[0].disabled = null
```

注入 Javascript 可以使用快捷指令（aka. 捷径），也可以使用 [JSBox 脚本](enable-button.js)。

随后提交 token，获得 flag。