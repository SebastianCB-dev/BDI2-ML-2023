
export const joinClasses = (classes: string, element?: string): string => {
  const classArray = classes.split(' ')
  if (element !== null && element !== undefined && element !== '') {
    classArray.unshift(element)
  }
  return classArray.join('.')
}
