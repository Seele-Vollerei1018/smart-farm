<template>
  <!-- 小测试 -->
  <section class="content-card quiz-section">

    <div class="section-title-row">
      <h2 class="section-title">🧪 小测试</h2>
      <span class="section-subtitle">
        做一道轻量题目，马上检验学习效果
      </span>
    </div>

    <div class="quiz-box">

      <!-- 题目 -->
      <div class="quiz-question">
        {{ currentQuiz.question }}
      </div>

      <!-- 选项 -->
      <div class="quiz-options">
        <button
          v-for="(option, index) in currentQuiz.options"
          :key="index"
          class="quiz-option"
          :class="getOptionClass(option)"
          @click="$emit('checkAnswer', option)"
          :disabled="quizAnswered"
        >
          {{ option }}
        </button>
      </div>

      <!-- 结果 -->
      <transition name="fade-slide">
        <div
          v-if="quizAnswered"
          class="quiz-result"
          :class="{ correct: isCorrect, wrong: !isCorrect }"
        >
          <div class="quiz-result-title">
            {{ isCorrect ? '✅ 回答正确！' : '❌ 回答不对，再想想' }}
          </div>

          <div class="quiz-result-desc">
            {{ currentQuiz.explanation }}
          </div>
        </div>
      </transition>

      <!-- 操作 -->
      <div class="quiz-action-row">

        <button
          class="ghost-btn"
          @click="$emit('resetQuiz')"
        >
          重新作答
        </button>

        <button
          class="primary-btn"
          @click="$emit('askQuizAI')"
        >
          🤖 让 AI 讲讲这题
        </button>

      </div>

    </div>

  </section>
</template>

<script setup>
defineProps({
  currentQuiz: Object,
  quizAnswered: Boolean,
  isCorrect: Boolean,
  selectedAnswer: String,
  getOptionClass: Function
})

defineEmits([
  'checkAnswer',
  'resetQuiz',
  'askQuizAI'
])
</script>

<style scoped>
.quiz-box {
  border-radius: 20px;
  padding: 22px;

  background: #f8fcf8;
  border: 1px solid rgba(76,175,80,0.12);

  box-shadow: 0 8px 20px rgba(0,0,0,0.05);
}

/* 题目 */
.quiz-question {
  font-size: 22px;
  font-weight: 800;
  margin-bottom: 16px;
}

/* 选项 */
.quiz-option {
  padding: 14px;
  border-radius: 14px;
  border: 1px solid #eee;
  background: #fff;
  cursor: pointer;
  transition: 0.25s;
}

.quiz-option:hover {
  transform: translateY(-2px);
  border-color: #4caf50;
}

/* 正确错误 */
.right-answer {
  background: rgba(76,175,80,0.12);
  border-color: #4caf50;
}

.wrong-answer {
  background: rgba(244,67,54,0.08);
  border-color: #e53935;
}

/* 结果 */
.quiz-result {
  margin-top: 18px;
  padding: 12px;
  border-radius: 12px;
  background: #fff;
}
</style>