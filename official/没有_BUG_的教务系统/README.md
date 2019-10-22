# 没有 BUG 的教务系统

## 0x00 杂谈

这道题灵感和漏洞来自 pwnable.tw 的一道题目(pwnable.tw 不允许公布高分题 wp， 所以笔者不说具体是哪道题)。

正巧妮可的新教务系统垃圾的要命，于是出题人决定高端黑一波妮可的教务系统。

最终，出题人在 3 个小时内完成了这个整整 200 行的教务系统（可能这个时间比外包公司完成妮可的教务系统还长）。

## 0x01 第一问

第一问是一道简单的逆向，笔者看到有很多选手都做了，证明这问不太难。

Python 脚本见`exp0.py`.

## 0x02 第二问

**萌新可以跳过，这一问需要一定的 pwn 积累。**

### 漏洞

这题的最难的地方就是找到洞在哪。笔者第一次做 pwnable.tw 上那道题目时盯着代码看了一天也没找到洞(哭)。

究其原因，是因为给了源代码。

如果不给源代码，笔者有自信在4小时内找到洞在哪.........

这种痛苦不能让笔者一个人承担，所以这道题也给了源代码 (理直气壮)

言归正传，这题洞主要在 C++ 的 C++ 等号运算符重载的编写。我想对于 C++ 老手来说这个地方肯定一眼就能看出来。以下详细解释一下。

```c++
        Grade operator=(const Grade &g) {
            studentNum = new char[strlen(g.studentNum) + 1];
            strcpy(studentNum, g.studentNum);
            calculusGrade = g.calculusGrade;
            linearAlgebraGrade = g.linearAlgebraGrade;
            mechanicsGrade = g.mechanicsGrade;
            cryptographyGrade = g.cryptographyGrade;
        }
```

这段代码对于 C++ 初学者来说，很难看出什么问题，对于很多 C++ 老鸟来说看出来有问题，也知道怎么改，但是也很难想到怎么利用。

问题的关键在于返回值。正确的写法应该是这样的。

```c++
        Grade& operator=(const Grade &g) {
            studentNum = new char[strlen(g.studentNum) + 1];
            strcpy(studentNum, g.studentNum);
            calculusGrade = g.calculusGrade;
            linearAlgebraGrade = g.linearAlgebraGrade;
            mechanicsGrade = g.mechanicsGrade;
            cryptographyGrade = g.cryptographyGrade;
            return this;
        }
```

相信很多朋友已经知道问题了。C/C++ 在函数返回的时候，返回值都是用 eax/rax 装的，但是如果是可变大小的类呢？一般来说有两种方法：

1. 返回地址
2. 返回值通过参数传递

可能还有朋友不理解"返回值通过参数传递"是什么意思，我们接下来解释一下。

```c++
void swap(int *x, int *y) {
    int temp;
    temp = x;
    x = y;
    y = temp;
}
```

我想以上代码大家都能理解，其实这个函数相当于有两个返回值，一个是 x，一个是 y。由于 x, y 不能直接返回(返回值只能有一个)，所以就通过参数返回了。

所以 我们在 IDA 里看到的这个错误的赋值函数的重载...是这样的...

```c++
__int64 __fastcall Grade::operator=(__int64 a1, __int64 a2, const char **a3)
{
  const char **v3; // ST08_8
  size_t v4; // rax

  v3 = a3;
  v4 = strlen(*a3);
  *(_QWORD *)a2 = operator new[](v4 + 1);
  strcpy(*(char **)a2, *v3);
  *(_DWORD *)(a2 + 8) = *((_DWORD *)v3 + 2);
  *(_DWORD *)(a2 + 12) = *((_DWORD *)v3 + 3);
  *(_DWORD *)(a2 + 16) = *((_DWORD *)v3 + 4);
  *(_DWORD *)(a2 + 20) = *((_DWORD *)v3 + 5);
  return a1;
}
```

`a2` 是 `this`, `a3` 是 `const Grade &g`，那么问题来了，`a1` 是啥呢？

这就是刚才说到的，`a1` 其实是返回值，由于 Grade 类的大小显然大于 8 byte，不能通过 rax 返回。所以程序会将这个返回的 Grade 的空间在栈上分配好，然后将这个栈上的地址传入函数作为参数。

这就是有趣的地方了。

```c++
unsigned __int64 editInfo(void)
{
  __int64 v0; // rbx
  __int64 v1; // rax
  __int64 v2; // rax
  char v4; // [rsp+0h] [rbp-50h]
  char v5; // [rsp+20h] [rbp-30h]
  unsigned __int64 v6; // [rsp+38h] [rbp-18h]

  v6 = __readfsqword(0x28u);
  Grade::Grade((Grade *)&v4);
  Grade::operator=((__int64)&v5, (__int64)&v4, (const char **)T);
  Grade::~Grade((Grade *)&v5);
  v0 = Grade::getStudentNum((Grade *)&v4);
  v1 = std::operator<<<std::char_traits<char>>(&std::cout, "STUDENT: ");
  v2 = std::operator<<<std::char_traits<char>>(v1, v0);
  std::ostream::operator<<(v2, &std::endl<char,std::char_traits<char>>);
  Grade::edit(T);
  Grade::~Grade((Grade *)&v4);
  return __readfsqword(0x28u) ^ v6;
}
```

让我们看看在 editInfo 的时候，程序做了什么有趣的事情。

首先，在栈上分配了一段 v5。

然后在 `Grade::operator=((__int64)&v5, (__int64)&v4, (const char **)T);` 中对 `v5` 什么都没做。

然后..... 就在 `Grade::~Grade((Grade *)&v5);` 中把 `*v5` 给 free 掉了....

而恰巧，这个地址我们是可以写入的。因为之前调用了 `setPassword` 函数，而栈上的 `char temp_password[0xa0];` 又没有被清空。

**所以，这就是一个任意地址 free!**

### 利用

#### 泄露 heap addr

因为 password 会被拷贝到 bss 段，而且没有 PIE，所以 bss 的地址是知道的。所以在 bss 段上面构造 chunk，free 掉之后就能通过 fastbin 链看到链上上一个 chunk 的地址。

#### 泄露 libc addr

泄露 libc 相对而言更具技巧性。我们把 T 所在的 chunk free 掉，然后再 malloc 回来，并在 `studentNum` 对应的位置写上 got 表地址。当程序打印 `studentNum` 的时候，`studentNum` 的地址已经被我们替换成了 got 表的地址，淫才可以泄露出已调用的函数的 libc 地址（例如 exp 中的 `setvbuf`）

#### Get Shell

这一步就容易的多了，通过 UAF，打到 malloc_hook，使用 one_gadget 来 getshell。过程见 exp。