<template>
  <div id="app">
    <ChatBox />
  </div>
</template>

<script>
import ChatBox from './components/ChatBox.vue';

export default {
  name: 'App',
  components: {
    ChatBox
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

#app {
  width: 100%;
  height: 100vh;
}
</style>