import { DEFAULT_FOLDER_LOGS } from '@src/constants/files.constant'
import { Environments } from '@src/interface/environments'
import { red, blue, yellow } from 'colors'
import { createLogger, transports, format, Logger } from 'winston'

export class LoggerService {
  private readonly _folder: string = DEFAULT_FOLDER_LOGS
  private _logger: Logger | undefined = undefined

  constructor () {
    this.initializeLogger()
  }

  /**
   * Initializes the Winston logger instance for the application.
   *
   * - Creates log files for errors and combined logs, named with the current date.
   * - Sets the log level to 'info' and uses JSON formatting for file logs.
   * - Adds default metadata indicating the service name.
   * - In non-production environments, also logs to the console with a simple format.
   *
   * @private
   */
  private initializeLogger (): void {
    const currentDate = new Date().toISOString().split('T')[0]
    this._logger = createLogger({
      level: 'info',
      format: format.json(),
      defaultMeta: { service: 'Microservice-Get-Users' },
      transports: [
        new transports.File({
          filename: `${this._folder}/error-${currentDate}.log`,
          level: 'error'
        }),
        new transports.File({
          filename: `${this._folder}/combined-${currentDate}.log`
        })
      ]
    })

    if (process.env.ENVIRONMENT !== Environments.PRODUCTION) {
      this._logger.add(
        new transports.Console({
          format: format.simple()
        })
      )
    }
  }

  /**
   * Logs an error message using the configured logger.
   * If the logger is not initialized, outputs an error to the console.
   *
   * @param message - The error message to log.
   */
  public errorLog (message: string): void {
    if (this._logger === undefined) {
      console.error(red('Logger not initialized'))
      return
    }
    this._logger.error({
      level: 'error',
      message: red(message),
      timestamp: new Date().toISOString()
    })
  }

  /**
   * Logs an informational message using the configured logger.
   *
   * @param message - The message to log.
   * @remarks
   * If the logger is not initialized, an error is printed to the console.
   * The log entry includes the log level, the message (styled in blue), and a timestamp.
   */
  public infoLog (message: string): void {
    if (this._logger === undefined) {
      console.error(red('Logger not initialized'))
      return
    }
    this._logger.info({
      level: 'info',
      message: blue(message),
      timestamp: new Date().toISOString()
    })
  }

  /**
   * Logs a warning message using the configured logger.
   *
   * If the logger is not initialized, outputs an error to the console.
   * The warning message is colorized in yellow and includes a timestamp.
   *
   * @param message - The warning message to log.
   */
  public warningLog (message: string): void {
    if (this._logger === undefined) {
      console.error(red('Logger not initialized'))
      return
    }
    this._logger.warn({
      level: 'warn',
      message: yellow(message),
      timestamp: new Date().toISOString()
    })
  }
}
