<template>
  <div class="level-tabs">
    <div
      v-for="item in levels"
      :key="item.value"
      class="tab"
      :class="{ active: modelValue === item.value }"
      @click="$emit('update:modelValue', item.value)"
    >
      {{ item.label }}
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: String
})

const levels = [
  { label: '基础认知', value: 'primary' },
  { label: '农业知识', value: 'middle' },
  { label: '智慧农业', value: 'advanced' }
]
</script>

<style scoped>
.level-tabs {
  display: flex;
  gap: 12px;
  padding: 10px 20px;
}

.tab {
  padding: 6px 14px;
  border-radius: 20px;
  background: #f2f5f3;
  cursor: pointer;
}

.tab.active {
  background: #8BA888;
  color: white;
}
</style>