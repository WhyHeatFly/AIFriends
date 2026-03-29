<script setup>

import {useRoute, useRouter} from "vue-router";

const route = useRoute()   // route 拿到当前路由的相关信息，返回的是当前路由对象
const router = useRouter() // router 拿到 "导航工具", 返回的是路由器实例，主要用来做“页面跳转”

</script>

<template>
个人空间: {{ route.params.user_id }}    <!- 取出user_id参数 >
</template>

<style scoped>

</style>