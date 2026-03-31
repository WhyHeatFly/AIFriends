<script setup>

import {onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CarmeraIcon from "@/views/user/profile/components/icon/CarmeraIcon.vue";
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref('')

watch (() => props.photo, newVal => {
  myPhoto.value = newVal
}, { immediate: true })

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null


async function openModal(photo) {
  modalRef.value.showModal()

  if (!croppie) {
    croppie = new Croppie(croppieRef.value, {
      viewport: {width: 200, height: 200, type: 'square'},
      boundary: {width: 300, height: 300},
      enableOrientation: true,
      enforceBoundary: true,
    })
  }

  croppie.bind({
    url: photo,
  })
}

// 处理图片上传
function onFileChange(e) { //文件选择变化事件的处理函数 绑定在change事件上 <input type="file" @change="onFileChange">
  // e 就是事件对象，里面记录了“这次 change 事件”的相关信息。
  /*
  const file = e.target.files[0] 这里是在获取用户刚刚选择的文件。
  e.target：触发事件的那个元素，也就是文件上传框 <input type="file">
  e.target.files：用户选中的文件列表
  e.target.files[0]：第一个文件
  */
  const file = e.target.files[0]
  // 把文件输入框清空。因为如果不清空，用户下一次再选择同一个文件时，浏览器可能认为“还是这个文件，没变化”，于是 change 事件不会再次触发。
  e.target.value = ''
  /*这一步是在做保护。意思是：
  如果用户没有选文件
  或者选择文件后又取消了
  那就直接结束函数。因为这时候 file 是 undefined，后面就没必要继续读文件了。*/
  if (!file) return
  /* 这里创建了一个 FileReader 对象。FileReader 是浏览器提供的 API，用来读取本地文件内容。*/
  const reader = new FileReader()

  /*这一步是在注册“读取完成后的回调函数”。因为文件读取不是瞬间完成的，而是异步的。
  也就是：
  你发起读取
  浏览器慢慢读
  读完以后才执行 onload
  这里的意思就是：当文件读取成功后，把读取结果 reader.result 传给 openModal()*/
  reader.onload = () => {
    openModal(reader.result)
  }

  /*这一步才是真正开始读取文件。
  readAsDataURL(file) 的含义是：把文件读取成一个 Base64 的 Data URL 字符串*/
  reader.readAsDataURL(file)
}

// 裁剪图片
async function crop() {
  if (!croppie) return

  myPhoto.value = await croppie.result({
    type: 'base64',
    size: 'viewport',
  })

  modalRef.value.close()
}

onBeforeUnmount(() => {
  croppie?.destroy()
})

defineExpose({
  myPhoto,
})

</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div v-if="myPhoto" class="w-28 rounded-full">
        <img :src="myPhoto" alt="">
      </div>
      <div v-else class="w-28 h-28 rounded-full bg-base-200"></div>
      <div @click="fileInputRef.click()" class="w-28 h-28 rounded-full bg-black/20 absolute left-0 top-0 flex justify-center items-center cursor-pointer">
        <CarmeraIcon/>
      </div>
    </div>
  </div>

  <input ref="file-input-ref" type="file" class="hidden" accept="image/*" @change="onFileChange">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
      <button @click="modalRef.close()" class="btn btn-lg btn-circle btn-ghost absolute right-2 top-2">×</button>

      <div ref="croppie-ref" class="flex flex-col my-4"></div>

      <div class="modal-action">
        <button @click="modalRef.close()" class="btn">取消</button>
        <button @click="crop" class="btn btn-neutral">确定</button>
      </div>
    </div>
  </dialog>

</template>

<style scoped>

</style>