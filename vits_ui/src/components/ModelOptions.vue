<template>
  <div class="model-option-wrapper">
    <ModelCard class="model-card" v-for="item of checkpoints" :modelOpention="item" :key="item.model"
      :selected="item.model == selectedItem.model" @click="handleClick(item)">
    </ModelCard>
  </div>
</template>

<script setup>
import { reactive, ref, watch, onMounted, computed } from 'vue';
import ModelCard from './ModelCard.vue';
const props = defineProps({
  checkpoints: {
    type: Array,
    default() {
      return [
      ]
    }
  },
  value: {
    type: String,
    default() {
      return "chilloutmix"
    }
  }
})
const selectedItem = ref({})
const emits = defineEmits(["update:value"])
if (props.checkpoints.length > 0) {
  selectedItem.value = props.checkpoints[0]
  if (selectedItem.value) {
    emits("update:value", selectedItem.value.model)
  }
}
watch(() => {
  return props.checkpoints
}, (newVal) => {
  if (newVal.length > 0) {
    selectedItem.value = newVal[0]
    if (selectedItem.value) {
      emits("update:value", selectedItem.value.model)
    }
  } else {
    selectedItem.value = {}
  }
})

const handleClick = (item) => {
  selectedItem.value = item
  console.log(item.model)
  emits("update:value", item.model)
}


</script>


<style scoped >
.model-option-wrapper {
  width: 100%;
  padding: 4px;
  height: 108px;
  display: flex;
  flex-direction: row;
  justify-content: left;
  align-items: center;
}

.model-card {
  margin-right: 8px;
}
</style>
