<template>
  <div id="app">
    <Flag :happyFlag="B64Flag"/>
  </div>
</template>

<script>
import Flag from './components/Flag.vue'

export default {
  name: 'app',
  components: {
    Flag
  },
  data: function () {
    return {
        B64Flag: 'ZmxhZ3tXZWxjb21lX3RvX0hhY2tlcmdhbWVfMjAxOQ=='
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  color: #2c3e50;
  margin-top: 40px;
}
</style>
