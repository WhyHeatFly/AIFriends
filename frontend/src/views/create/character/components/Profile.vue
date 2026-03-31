<script setup>

import {ref, watch} from "vue";

const props = defineProps(['profile'])
const myProfile = ref('')

watch(() => props.profile, newVal => {
  myProfile.value = newVal
}, { immediate: true })

defineExpose({
  myProfile,
})

</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base">角色简介</label>
    <textarea v-model="myProfile" rows="6" class="textarea w-108"></textarea>
  </fieldset>
</template>

<style scoped>

</style>