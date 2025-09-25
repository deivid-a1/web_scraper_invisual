const winston = require('winston');
const path = require('path');

function setupLogger(executionPath) {
    const logDir = path.join(executionPath, 'log');
    const logFilename = 'execution.log';
    const logPath = path.join(logDir, logFilename);

    const fs = require('fs');
    if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
    }

    const logger = winston.createLogger({
        level: 'info',
        format: winston.format.combine(
            winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
            winston.format.printf(({ timestamp, level, message, ...meta }) => {
                const service = meta.service || 'app';
                return `${timestamp} - [${service}] - ${level.toUpperCase()} - ${message}`;
            })
        ),
        transports: [
            new winston.transports.File({ filename: logPath, mode: 'w' }),
            new winston.transports.Console()
        ]
    });

    return logger;
}

module.exports = { setupLogger };