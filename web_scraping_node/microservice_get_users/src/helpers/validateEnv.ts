import { LoggerService as Logger } from '@src/classes'
import { ENV_VARIABLES, ENV_VALUES_RUNTIME, NODE_ENV_VALUES } from '@src/constants/env'

/**
 * Validates the required environment variables for the application.
 *
 * Iterates through the list of required environment variables (`ENV_VARIABLES`)
 * and checks if each one is set and non-empty in `process.env`. Additionally,
 * for the environment variable specified by `NODE_ENV_VALUES.ENVIRONMENT`, it
 * verifies that its value is included in the allowed runtime values
 * (`ENV_VALUES_RUNTIME`). Logs informational messages for any missing or invalid
 * environment variables.
 *
 * @returns {boolean} `true` if all required environment variables are properly set and valid, otherwise `false`.
 */
export const validateEnv = (): boolean => {
  let existsEnv: boolean = true
  const logger: Logger = new Logger()

  ENV_VARIABLES.forEach((env: string) => {
    if (process.env[env] === undefined || process.env[env]?.length === 0) {
      logger.infoLog(`ℹ️ Environment variable '${env}' is not properly set`)
      existsEnv = false
    }
    if (env === NODE_ENV_VALUES.ENVIRONMENT && (!ENV_VALUES_RUNTIME.includes(process.env[env] ?? ''))) {
      logger.infoLog(`ℹ️ Environment variable '${env}' is not a valid value, please use one of the following values: ${ENV_VALUES_RUNTIME.join(', ')}`)
      existsEnv = false
    }
  })
  return existsEnv
}
