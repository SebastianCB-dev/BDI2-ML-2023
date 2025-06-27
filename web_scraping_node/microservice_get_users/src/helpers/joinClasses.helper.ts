
/**
 * Joins a string of CSS classes with an optional element, separating each part with a dot.
 *
 * @param classes - A string containing CSS class names separated by spaces.
 * @param element - An optional string representing an element to prepend to the class list.
 * @returns A string with the element (if provided) and class names joined by dots.
 *
 * @example
 * joinClasses('btn primary', 'button'); // returns 'button.btn.primary'
 * joinClasses('btn primary'); // returns 'btn.primary'
 */
export const joinClasses = (classes: string, element?: string): string => {
  const classArray = classes.split(' ')
  if (element !== null && element !== undefined && element !== '') {
    classArray.unshift(element)
  }
  return classArray.join('.')
}
