# Logging

Strefi logs with the python logging module. By default, logging level is set as "INFO" and the logs
are written in a file ".strefi.log" in the working directory. A backup saves 5 files of 10 MB.

If you want to configure logging yourself, you have to specify the path of the configuration file
(configparser file format) with the "-l" / "--log" argument.

```shell
strefi start -c config.json -l /path/to/log.conf
```

For more details on the configparser format, [read the docs](https://docs.python.org/3/library/logging.config.html#logging-config-fileformat).