import axios from 'axios';
import qs from 'qs';

export const request = function(url, type = 'get', data = {}, headers = {}, responseType = 'json') {
    const token = localStorage.getItem('token');
    const defaultHeaders = {
        ...headers,
    };

    if (token) {
        defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    let config = {
        method: type,
        url: url,
        headers: defaultHeaders,
        responseType: responseType === 'blob' ? 'blob' : 'json', // 根据参数设置响应类型
    };

    if (type === 'get' || type === 'delete') {
        config.params = data;
    } else {
        // 默认发送 JSON 数据，除非在 headers 中指定了其他 Content-Type
        if (!headers['Content-Type'] || headers['Content-Type'].indexOf('application/json') !== -1) {
            config.data = JSON.stringify(data);
            defaultHeaders['Content-Type'] = 'application/json'; // 确保 Content-Type 被正确设置
        } else if (headers['Content-Type'] === 'application/x-www-form-urlencoded') {
            config.data = qs.stringify(data);
        } else {
            // 其他 Content-Type 的情况，这里不做处理，调用者需要确保数据格式正确
            config.data = data;
        }
    }

    // 使用 axios 发送请求
    const axiosInstance = axios.create(); // 创建一个新的 axios 实例（可选，也可以直接使用 axios）
    return axiosInstance(config)
        .then(response => {
            if (responseType === 'blob') {
                return response.data; // 对于 Blob 响应，直接返回 Blob 对象
            } else {
                return response.data; // 对于 JSON 响应，返回解析后的数据
            }
        })
        .catch(error => {
            console.error('Request error:', error);
            throw error; // 重新抛出错误以便上层调用者可以捕获并处理
        });
};