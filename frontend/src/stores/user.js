// Vue3 + Pinia 里定义的一个 用户状态仓库（store）
// 在前端全局保存当前登录用户的信息，比如用户 id、用户名、头像、简介、accessToken。
import { ref } from 'vue'
import { defineStore } from 'pinia'

// 定义一个名字叫 'user' 的 store，并导出一个 useUserStore 函数。
// user 是这个 store 的唯一标识名， 也就是说，Pinia 内部知道这是一个叫 "user" 的仓库。
export const useUserStore = defineStore('user', ()=> {
    const id = ref(1)
    const username = ref('admin')
    const photo = ref('http://127.0.0.1:8000/media/user/photos/default.png')
    const profile = ref('111')
    const accessToken = ref('111')

    // 辅助函数判断是否处于登录状态
    function isLogin() {
        return !!accessToken.value
    }

    // 设置accessToken的值
    function setAccessToken(token) {
        accessToken.value = token
    }

    // 设置用户信息
    function setUserInfo(data) {
        id.value = data.user_id
        username.value = data.username
        photo.value = data.photo
        profile.value = data.profile
    }

    // 退出登录
    function logout() {
        id.value = 0
        username.value = ''
        photo.value = ''
        profile.value = ''
        accessToken.value = ''
    }
    return {
        id,
        username,
        photo,
        profile,
        accessToken,
        isLogin,
        setAccessToken,
        setUserInfo,
        logout,
    }
})