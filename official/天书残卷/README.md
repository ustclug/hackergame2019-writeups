# hackergame 2019

## 天书残卷 writeup

花絮：原本出题人喜欢玩一玩正常的逆向，但是命题组不同意全部是一个类型的逆向，于是出题人只能找一找对所有人来说都是新鲜事物的whitespace作为逆向语言。

whitespace是一个十分神奇的语言。Whitespace却只视空格 （space）、 制表符 （tabs）和换行 （new lines）为语法的一部分，它的直译器忽略所有非空白字元。

这些字符都是不可见字符，所以像天书一样难以理解。

我们拿winhex或者010editor这种好用的文本编辑器打开。

使用以下whitespace反汇编器。

```html
https://vii5ard.github.io/whitespace/
```

将我们的whitespace代码复制到它的输入框。

我们将得到以下结果。

```assembly
push 10
call label_0
push 0
push 58
push 103
push 97
push 108
push 102
push 32
push 114
push 117
push 111
push 121
push 32
push 116
push 117
push 112
push 110
push 105
push 32
push 101
push 115
push 97
push 101
push 108
push 80
call label_1
call label_2
call label_3
label_4:
push 2
add
push 127
sub
jz label_5
jmp label_6
label_5:
push 2
add
push 53
sub
jz label_7
jmp label_6
label_7:
push 2
add
push 105
sub
jz label_8
jmp label_6
label_8:
push 2
add
push 54
sub
jz label_9
jmp label_6
label_9:
push 2
add
push 119
sub
jz label_10
jmp label_6
label_10:
push 2
add
push 105
sub
jz label_11
jmp label_6
label_11:
push 2
add
push 112
sub
jz label_12
jmp label_6
label_12:
push 2
add
push 54
sub
jz label_13
jmp label_6
label_13:
push 2
add
push 110
sub
jz label_14
jmp label_6
label_14:
push 2
add
push 97
sub
jz label_15
jmp label_6
label_15:
push 2
add
push 111
sub
jz label_16
jmp label_6
label_16:
push 2
add
push 54
sub
jz label_17
jmp label_6
label_17:
push 2
add
push 116
sub
jz label_18
jmp label_6
label_18:
push 2
add
push 105
sub
jz label_19
jmp label_6
label_19:
push 2
add
push 50
sub
jz label_20
jmp label_6
label_20:
push 2
add
push 116
sub
jz label_21
jmp label_6
label_21:
push 2
add
push 114
sub
jz label_22
jmp label_6
label_22:
push 2
add
push 97
sub
jz label_23
jmp label_6
label_23:
push 2
add
push 118
sub
jz label_24
jmp label_6
label_24:
push 2
add
push 110
sub
jz label_25
jmp label_6
label_25:
push 2
add
push 119
sub
jz label_26
jmp label_6
label_26:
push 2
add
push 101
sub
jz label_27
jmp label_6
label_27:
push 2
add
push 107
sub
jz label_28
jmp label_6
label_28:
push 2
add
push 104
sub
jz label_29
jmp label_6
label_29:
push 2
add
push 104
sub
jz label_30
jmp label_6
label_30:
push 2
add
push 107
sub
jz label_31
jmp label_6
label_31:
push 2
add
push 102
sub
jz label_32
jmp label_6
label_32:
push 2
add
push 97
sub
jz label_33
jmp label_6
label_33:
push 2
add
push 99
sub
jz label_34
jmp label_6
label_34:
push 2
add
push 97
sub
jz label_35
jmp label_6
label_35:
push 2
add
push 117
sub
jz label_36
jmp label_6
label_36:
push 2
add
push 107
sub
jz label_37
jmp label_6
label_37:
push 2
add
push 97
sub
jz label_38
jmp label_6
label_38:
push 2
add
push 53
sub
jz label_39
jmp label_6
label_39:
push 2
add
push 101
sub
jz label_40
jmp label_6
label_40:
push 2
add
push 54
sub
jz label_41
jmp label_6
label_41:
push 2
add
push 114
sub
jz label_42
jmp label_6
label_42:
push 2
add
push 117
sub
jz label_43
jmp label_6
label_43:
push 2
add
push 53
sub
jz label_44
jmp label_6
label_44:
push 2
add
push 118
sub
jz label_45
jmp label_6
label_45:
push 2
add
push 107
sub
jz label_46
jmp label_6
label_46:
push 2
add
push 106
sub
jz label_47
jmp label_6
label_47:
push 2
add
push 89
sub
jz label_48
jmp label_6
label_48:
push 2
add
push 125
sub
jz label_49
jmp label_6
label_49:
push 2
add
push 105
sub
jz label_50
jmp label_6
label_50:
push 2
add
push 99
sub
jz label_51
jmp label_6
label_51:
push 2
add
push 110
sub
jz label_52
jmp label_6
label_52:
push 2
add
push 104
sub
jz label_53
jmp label_6
label_53:
push 0
push 33
push 115
push 110
push 111
push 105
push 116
push 97
push 108
push 117
push 116
push 97
push 114
push 103
push 110
push 111
push 67
call label_1
end
label_6:
push 0
push 33
push 116
push 99
push 101
push 114
push 114
push 111
push 99
push 110
push 105
push 32
push 115
push 105
push 32
push 103
push 97
push 108
push 102
push 32
push 114
push 117
push 111
push 121
push 32
push 107
push 110
push 105
push 104
push 116
push 32
push 73
call label_1
end
label_0:
push 2
add
push 0
swap
store
ret
label_54:
dup
jz label_55
printc
jmp label_54
label_55:
drop
ret
label_1:
call label_54
push 0
push 10
printc
ret
label_2:
push 0
push 0
retrieve
dup
push 1
add
push 0
swap
store
push 0
store
label_56:
push 1
readc
push 1
retrieve
dup
push 10
sub
jz label_57
jmp label_56
label_58:
drop
label_57:
dup
push 10
sub
jz label_58
dup
push 0
retrieve
dup
push 1
add
push 0
swap
store
swap
store
jz label_59
jmp label_57
label_59:
push 0
retrieve
push 1
sub
push 0
swap
store
ret
label_3:
push 0
retrieve
push 2
sub
jz label_60
label_61:
push 0
retrieve
push 1
sub
dup
push 0
swap
store
retrieve
dup
jz label_60
jmp label_61
label_60:
drop
ret
label_62:
jz label_63
jmp label_62
label_63:
ret
```

主要关注label4-label52之间的内容。仔细阅读会发现很简单。把输入的字符的ascii与2相加，然后与要对比的ascii相减，如果等于0则说明该输入的字符正确。否则会输出不正确。所以最后的flag就是label4-label52之间被压栈的数字减2的ASCII。
