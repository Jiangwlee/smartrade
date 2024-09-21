/**
 * 将日期字符串格式化成时间字符串.
 * 
 * @param time ISO 日期-时间字符串.
 * @returns HH:MM:SS 格式的时间
 */
function formatTime(time: string) {
  if (time === '') {
    return ''
  } else {
    let datetime = new Date(time)
    const hour = datetime.getHours().toString().padStart(2, '0')
    const minutes = datetime.getMinutes().toString().padStart(2, '0')
    const seconds = datetime.getSeconds().toString().padStart(2, '0')
    return `${hour}:${minutes}:${seconds}`
  }
}

export {
    formatTime
}
