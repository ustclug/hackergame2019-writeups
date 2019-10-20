<template>
  <div class="hello">
    <h1>签到题</h1>
    <label>你的 token:
      <input type="text" v-model.trim="token">
    </label>
    <br>
    <br>
    <button disabled @click="showFlag">点击此处，获取 flag</button>
    <h3 v-show="isFlagVisible">{{ realFlag }}</h3>
    <p>Notice:</p>
    <ol>
      <li>请确保 token 输入正确（<b>你可以使用平台的「复制」按钮，确保粘贴后 token 的正确性</b>），否则可能出现错误的 flag。</li>
      <li><b>请不要使用其他人的 token。</b></li>
      <li>什么？你说点不了按钮？或许你可以去参考一下
        <a href="https://github.com/ustclug/hackergame2018-writeups/blob/master/official/qiandao/README.md#%E8%A7%A3%E6%B3%95%E4%BA%8C%E5%AE%A1%E6%9F%A5%E5%85%83%E7%B4%A0">
          去年签到题的题解 (writeup)</a>。</li>
      <li>此外，我们建议你使用一台电脑完成本比赛的题目，否则可能会遇到比较大的困难。</li>
    </ol>
  </div>
</template>

<script>
import CryptoJS from "crypto-js";

export default {
  name: 'Flag',
  props: {
    happyFlag: String
  },
  data: function () {
    return {
      isFlagVisible: false,
      realFlag: "Please click the button to get the flag.",
      token: null
    }
  },
  methods: {
    showFlag: function () {
      if (this.token) {
        this.realFlag = atob(this.happyFlag);
        this.processedToken = CryptoJS.SHA1(this.token).toString(CryptoJS.enc.Hex).substring(0, 10);
        this.realFlag = this.realFlag.substring(0, this.realFlag.length) + "_"
                + this.processedToken + "}";
        this.isFlagVisible = true
      } else {
        this.realFlag = "请输入 token。";
        this.isFlagVisible = true
      }
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
a {
  color: #42b983;
}
input {
  width: 50%;
}
</style>
