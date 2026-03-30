<script setup>

// 在子组件接受参数
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CarmeraIcon from "@/views/user/profile/components/icon/CarmeraIcon.vue";
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

// 监视某个值的变化，然后在变化时执行回调
// () => props.photo 这是一个 getter 函数, 用来监听 props.photo 的值，这里必须写成函数形式
// newVal => { myPhoto.value = newVal } 这是监听到变化后要执行的回调函数
// 含义是：当 props.photo 变化时, 把变化后的新值 newVal, 赋给 myPhoto.value

watch(() => props.photo, newVal => {
  myPhoto.value = newVal
})

defineExpose({
  myPhoto,
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

async function openModal(photo) {
  modalRef.value.showModal()

  await nextTick()

  if (!croppie) {
    croppie = new Croppie(croppieRef.value, {  // 创建 croppie 对象
      viewport: {width: 200, height: 200, type: 'square'},
      boundary: {width: 300, height: 300},
      enableOrientation: true,
      enforceBoundary: true,
    })
  }

  croppie.bind({ // 绑定裁剪图片
    url: photo
  })
}

// 裁剪图片
async function crop() {
  if (! croppie) return

  myPhoto.value = await croppie.result({
    type: 'base64',
    size: 'viewport',
  })

  modalRef.value.close()
}

function onFileChange(e) {
  const file = e.target.files[0]
  e.target.value = ''
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    openModal(reader.result)
  }
  reader.readAsDataURL(file)
}

// 在组件卸载前释放croppie对象，防止内存泄漏
onBeforeUnmount(() => {
  croppie?.destroy()
})

</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div class="w-28 rounded-full">
        <img :src="myPhoto" alt="">
      </div>
      <div @click="fileInputRef.click()" class="absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
        <CarmeraIcon/>
      </div>
    </div>
  </div>

  <input ref="file-input-ref" type="file" accept="image/*" class="hidden" @change="onFileChange">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
      <button @click="modalRef.close()" class="btn btn-circle btn-lg btn-ghost absolute right-2 top-2">×</button>
      <!-- 定义 croppie 绑定的标签 -->
      <div ref="croppie-ref" class="flex flex-col justify-center my-4"></div>

      <div class="modal-action">
        <button @click="modalRef.close()" class="btn">取消</button>
        <button @click="crop" class="btn btn-neutral">确定</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

</style>