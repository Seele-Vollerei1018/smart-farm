const AMAP_KEY = import.meta.env.VITE_AMAP_KEY || 'default_key'

// 导入城市编码映射表
import cityCodeMap from './cityCodes'

export { cityCodeMap }

/**
 * 获取城市天气数据
 * @param {string} cityName - 城市名称
 * @returns {Promise<Object>} 天气数据对象
 */
export async function fetchWeatherData(cityName) {
  if (!cityName) {
    throw new Error('请输入城市名称')
  }

  const cityCode = cityCodeMap[cityName]
  if (!cityCode) {
    throw new Error('暂不支持该城市，请尝试其他城市')
  }

  try {
    const response = await fetch(`https://restapi.amap.com/v3/weather/weatherInfo?key=${AMAP_KEY}&city=${cityCode}&extensions=base`)
    if (!response.ok) {
      throw new Error('网络请求失败')
    }

    const data = await response.json()
    if (data.status === '1' && data.lives && data.lives.length > 0) {
      const weatherData = data.lives[0]
      return {
        city: weatherData.city,
        temp: parseInt(weatherData.temperature),
        desc: weatherData.weather,
        humidity: parseInt(weatherData.humidity),
        wind: `${weatherData.winddirection} ${weatherData.windpower}级`,
        updated: new Date().toLocaleString('zh-CN', { hour12: false })
      }
    } else {
      throw new Error('获取天气数据失败')
    }
  } catch (err) {
    const error = new Error(`获取天气数据失败: ${err.message}`)
    error.cause = err
    throw error
  }
}
