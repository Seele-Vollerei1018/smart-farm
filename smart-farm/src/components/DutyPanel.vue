<template>
  <div class="duty-panel">
    <h2 class="title">🌾 今日值日生</h2>

    <div class="user">
      <img src="/avatar.png" class="avatar" />
      <div class="name">小农夫 · 张三</div>
    </div>

    <div class="tasks">
      <div 
        v-for="(task, index) in tasks" 
        :key="index"
        class="task"
        @click="toggleTask(index)"
      >
        <div class="checkbox" :class="{ done: task.done }"></div>
        <div class="text">{{ task.text }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const tasks = reactive([
  { text: "🌡️ 温湿度巡检完成，环境良好", done: false },
  { text: "🍅 西红柿除草完成", done: false },
  { text: "🧹 农具已归位", done: false }
])

const toggleTask = (i) => {
  tasks[i].done = !tasks[i].done
}
</script>

<style scoped>
.duty-panel {
  padding: 20px;
  background: #f9fbfa;
  height: 100%;
}

.title {
  font-size: 20px;
  color: #4caf50;
  margin-bottom: 20px;
}

.user {
  text-align: center;
  margin-bottom: 20px;
}

.avatar {
  width: 60px;
  border-radius: 50%;
}

.name {
  margin-top: 8px;
}

.task {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  cursor: pointer;
}

.checkbox {
  width: 18px;
  height: 18px;
  border: 2px solid #4caf50;
  border-radius: 50%;
  margin-right: 10px;
}

.checkbox.done {
  background: #4caf50;
}
</style>