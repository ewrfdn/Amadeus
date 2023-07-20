<template>
  <div class="container-wrapper">
    <div class="config-panel">
      <div class="params">
        <ParamsCard>
          <template v-slot:header><span>
              <span>模型</span>
            </span>
          </template>
          <template v-slot:content>
            <ModelOptions :checkpoints="checkpoints" v-model:value="params.model"></ModelOptions>
          </template>
        </ParamsCard>
        <ParamsCard>
          <template v-slot:header><span>
              <span>文本</span>
            </span>
          </template>
          <template v-slot:content>
            <a-textarea v-model:value="params.text" :autoSize="{ minRows: 4, maxRows: 6 }"></a-textarea>
          </template>
        </ParamsCard>

      </div>
      <div class="footer">
        <a-button class="generate-button" @click="generate" :loading="loading">生成</a-button>
      </div>
    </div>

    <div class="image-wrapper">
      <audio v-if="audioSrc" :src="audioSrc" controls></audio>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, toRaw, watch } from 'vue';
import ParamsCard from '../components/ParamsCard.vue';
import vits from "../api/vits"
import _ from "lodash"
import ModelOptions from '../components/ModelOptions.vue';
import { message } from 'ant-design-vue';
const params = reactive({
  model: "paimon",
  text: ""
})
const audioSrc = ref("")

const loading = ref(false)



const checkpoints = ref([
])
const generate = async () => {
  loading.value = true
  audioSrc.value = ""
  try {
    const data = { ...toRaw(params) }
    const res = await vits.text2Audio(data)
    console.log(typeof (res))
    const audioUrl = URL.createObjectURL(new Blob([res], { type: 'application/mp3,' }))
    audioSrc.value = audioUrl

  } catch (e) {
    message.error(e.toString())
    console.log(e)
  }
  loading.value = false
}

const getAllModel = async () => {
  try {
    const res = await vits.getAllVitsModel()
    checkpoints.value = _.map(res.list, (item) => {
      return {
        model: item.name,
        modelName: item.displayName
      }
    })
    console.log(checkpoints.value)

  } catch (e) {
    message.error(e.toString())
    console.log(e)
  }
}
getAllModel()
</script>


<style scoped >
.container-wrapper {
  display: flex;
  width: 100%;
  height: 100%;
  background: #eee;
  position: relative;
}

.title {
  font-size: 12px;
  color: #4e5969;
  padding-top: 4px;
  padding-bottom: 4px;
  width: 100%;
}

.config-panel {
  min-width: 300px;
  max-width: 640px;
  width: 45%;
  height: 100%;
  background: #fff;
}

.random-button {
  font-size: 12px !important;
  border-radius: 12px;
  margin-left: 12px;
}

.params {
  width: 100%;
  height: calc(100% - 72px);
  padding: 8px;
  display: flex;
  flex-direction: column;
  overflow: auto;
}

.generate-button {
  font-size: 15px;
  border-radius: 6px;
  bottom: 0px;
  width: calc(100% - 24px);
}

.footer {
  padding: 8px;
  height: 72px;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
}

.image-wrapper {
  flex: 1;
  padding: 16px
}

.image-view {
  width: 100%;
  height: 100%;
}
</style>
