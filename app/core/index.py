from app.core.config import settings

app_constants = {
	"loglevel_mapping": {
			"CRITICAL" : 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, "NOTSET": 0
	},
	"file_error" : "./logs/error.log",
	"file_info" : "./logs/info.log",
	"file_critical" : "./logs/critical.log",
	"file_warning" : "./logs/warning.log",
	"file_debug" : "./logs/debug.log",
}
