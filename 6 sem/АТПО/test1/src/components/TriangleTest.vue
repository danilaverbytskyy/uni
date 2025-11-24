<script setup>
import { ref } from "vue";

let side1 = ref("");
let side2 = ref("");
let side3 = ref("");
let answer = ref("");
let isAnswerCalculated = ref(false);
let isError = ref(false);
let msg = ref("");

function defineTriangle() {
  isError.value = false;
  isAnswerCalculated.value = false;
  answer.value = "";
  msg.value = "";

  // Преобразуем введённые данные в числа
  let numbers = [Number(side1.value), Number(side2.value), Number(side3.value)];

  // Проверяем, являются ли введённые значения числами и положительными
  if (numbers.some(isNaN) || numbers.some(num => num <= 0)) {
    msg.value = "Введите корректные числа";
    isError.value = true;
    return;
  }

  // Сортируем стороны по возрастанию
  numbers.sort((a, b) => a - b);

  // Проверяем неравенство треугольника
  if (numbers[0] + numbers[1] <= numbers[2]) {
    msg.value = "Стороны такой длины не образуют треугольник";
    isError.value = true;
    return;
  }

  // Определяем тип треугольника
  if (numbers[0] === numbers[1] && numbers[1] === numbers[2]) {
    answer.value = "Равносторонний";
  } else if (numbers[0] === numbers[1] || numbers[1] === numbers[2] || numbers[0] === numbers[2]) {
    answer.value = "Равнобедренный";
  } else if (numbers[0] ** 2 + numbers[1] ** 2 === numbers[2] ** 2) {
    answer.value = "Прямоугольный";
  } else {
    answer.value = "Обычный";
  }

  isAnswerCalculated.value = true;
}
</script>

<template>
  <div class="triangle-test">
    <div class="inline-triangle"><input v-model="side1" type="text" placeholder="Сторона 1"></div>
    <div class="inline-triangle"><input v-model="side2" type="text" placeholder="Сторона 2"></div>
    <div class="inline-triangle"><input v-model="side3" type="text" placeholder="Сторона 3"></div>
    <div class="inline-triangle">
      <button @click.prevent="defineTriangle">Определить тип</button>
    </div>
    <div class="inline-triangle red" v-if="isError">{{ msg }}</div>
    <div class="inline-triangle green" v-if="isAnswerCalculated">{{ answer }}</div>
  </div>
</template>

<style scoped>
.inline-triangle {
  display: flex;
  justify-content: center;
  margin: 5px;
}

.triangle-test {
  margin-top: 50px;
}

.red {
  color: darkred;
  font-size: 150%;
}

.green {
  color: darkgreen;
  font-size: 150%;
}
</style>
