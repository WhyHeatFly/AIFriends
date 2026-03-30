/*
 * 功能：在每个请求头里自动添加`access token`。
 * 然后拦截请求结果，如果返回结果是身份认证失败（401），
 * 则说明`access_token`过期了，
 * 那么先用`cookie`中的`refresh_token`刷新`access_token`。
 * 如果刷新失败则说明`refreh_token`也过期了，
 * 则调用`user.logout()`在浏览器内存中删除登录状态；
 * 如果刷新成功，则重新发送原请求。
*/

import axios from "axios"
import {useUserStore} from "@/stores/user.js";

const BASE_URL = 'http://127.0.0.1:8000'  // 后端基础地址

const api = axios.create({
    baseURL: BASE_URL,
    withCredentials: true, // 表示 跨域请求时，允许浏览器携带 cookie。
})

// 请求拦截器 自动添加 access_token
api.interceptors.request.use(config => {
    const user = useUserStore()
    if (user.accessToken) {
        config.headers.Authorization = `Bearer ${user.accessToken}`
    }
    return config
})

// 两个全局变量 控制刷新状态。 用来解决 如果多个请求同时发现 token 过期，不能让它们都去疯狂刷新 token。
let isRefreshing = false // 当前是否已经有一个“刷新 token”的请求正在进行中。
let refreshSubscribers = [] // 等待刷新的数组

/*
把一个回调函数放进等待队列里。
也就是：某个请求发现 token 过期了,它先别急着失败,它把“等刷新完成后我要干嘛”这件事注册进去,等刷新结束后统一执行
*/
function subscribeTokenRefresh(callback) {
    refreshSubscribers.push(callback)
}

/*
刷新成功后，把新的 token 通知给所有等待中的请求。
每个等待者收到新 token 后，就可以：给自己的原请求带上新 token重新发一次请求
最后再把等待队列清空。
*/
function onRefreshed(token) {
    refreshSubscribers.forEach(cb => cb(token))
    refreshSubscribers = []
}

/*
如果刷新失败了，就告诉所有等待中的请求：别等了，失败了。
这些等待的请求收到失败信息后，就会各自 reject。
*/
function onRefreshFailed(err) {
    refreshSubscribers.forEach(cb => cb(null, err))
    refreshSubscribers = []
}


api.interceptors.response.use(
    response => response, // 成功响应 原样返回

    async error => {
        const user = useUserStore() // 拿当前用户 store
        const originalRequest = error?.config  // 拿到这次失败的原始请求配置
        if (!originalRequest) {
            return Promise.reject(error)
        }

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            return new Promise((resolve, reject) => {
                subscribeTokenRefresh((token, error) => {
                    if (error) {
                        reject(error)
                    } else {
                        originalRequest.headers.Authorization = `Bearer ${token}`
                        resolve(api(originalRequest))
                    }
                })

                if (!isRefreshing) {
                    isRefreshing = true
                    axios.post(
                        `${BASE_URL}/api/user/account/refresh_token/`,
                        {},
                        {withCredentials: true, timeout: 5000}
                    ).then(res => {
                        user.setAccessToken(res.data.access)
                        onRefreshed(res.data.access)
                    }).catch(error => {
                        user.logout()
                        onRefreshFailed(error)
                        reject(error)
                    }).finally(() => {
                        isRefreshing = false
                    })
                }
            })
        }

        return Promise.reject(error)
    }
)

export default api