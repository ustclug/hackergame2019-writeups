```
char c1 = ((Character)((Iterator)localObject2).next()).charValue();
        localObject3 = new java/lang/StringBuilder;
        ((StringBuilder)localObject3).<init>();
        ((StringBuilder)localObject3).append((String)localObject1);
        char c2;
        char c3;
        if (Character.isUpperCase(c1))
        {
          c2 = Character.toLowerCase(c1);
          c3 = c2;
        }
        else
        {
          c3 = c1;
          if (Character.isLowerCase(c1))
          {
            c2 = Character.toUpperCase(c1);
            c3 = c2;
          }
        }
        ((StringBuilder)localObject3).append(c3);
        localObject1 = ((StringBuilder)localObject3).toString();
      }
      Log.d("pass1", (String)localObject1);
      localObject2 = login.1.INSTANCE;
      if (Intrinsics.areEqual(localObject1, "AgfJA2vYz2fTztiWmtL3AxrOzNvUiq=="))
```
只截取了一部分,仔细看就会发现,大小写互相转换,然后base64比较,所以逆过来把大小写转换回来,就能得到
aGFja2VyZ2FtZTIwMTl3aXRoZnVuIQ==

base64解码得到密码

hackergame2019withfun
