import { red, blue, yellow } from 'colors'
import { createLogger, transports, format, Logger } from 'winston'

export class LoggerService {
  private readonly _logger: Logger

  constructor () {
    this._logger = createLogger({
      level: 'info',
      format: format.json(),
      defaultMeta: { service: 'Microservice-Get-Users' },
      transports: [
        new transports.File({ filename: 'error.log', level: 'error' }),
        new transports.File({ filename: 'combined.log' })
      ]
    })

    if (process.env.ENVIRONMENT !== 'production') {
      this._logger.add(new transports.Console({
        format: format.simple()
      }))
    }
  }

  public errorLog (message: string): void {
    this._logger.error({
      level: 'error',
      message: red(message),
      timestamp: new Date().toISOString()
    })
  }

  public infoLog (message: string): void {
    this._logger.info({
      level: 'info',
      message: blue(message),
      timestamp: new Date().toISOString()
    })
  }

  public warningLog (message: string): void {
    this._logger.warn({
      level: 'warn',
      message: yellow(message),
      timestamp: new Date().toISOString()
    })
  }
}
