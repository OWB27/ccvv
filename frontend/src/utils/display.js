export function displayValue(value, fallback = '未识别') {
  if (value === null || value === undefined || value === '') {
    return fallback
  }
  return value
}

export function isNonEmptyArray(value) {
  return Array.isArray(value) && value.length > 0
}

