import {red, blue, yellow} from 'colors'

export class Logger {
  static errorLog(message: string): void {
    console.log (red (message))
  }

  static infoLog(message: string): void {
    console.log (blue (message))
  }

  static warningLog(message: string): void {
    console.log (yellow (message))
  }
}
