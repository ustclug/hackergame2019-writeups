# 没有 BUG 的教务系统

因为是分析登陆部分，所以直接定位到 `main` 函数，发现它将密码拷贝到新数组 `temp_password` 中，并循环对前八位进行某些操作后与另一长度为 9 的字符串比较判断密码是否正确，说明原密码第 9 位与该字符串一样，均为 `'\0'`。

接着分析该操作，发现是将 `temp_password[i]`、`temp_password[i + 1]` 和 `i` 进行位运算之后赋值给 `temp_password[i]`。列出该位运算的真值表可知其等价于 `temp_password[i] ^ temp_password[i + 1] ^ i` ，也即整个语句等效于 `temp_password[i] ^= temp_password[i + 1] ^ i;`。由异或操作的性质可知，逆序进行同样的操作即可“还原”该字符串。

编写[程序](revert.c)对该字符串进行还原，得到教务系统密码，即 flag1。

水平太菜，解不出 flag2。