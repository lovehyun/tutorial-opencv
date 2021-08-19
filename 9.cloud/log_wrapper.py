import logging

# Logging
def create_logger(name, level):
    logger = logging.getLogger(name)

    if len(logger.handlers) > 0:
        return logger

    # DEBUG < INFO < WARNING(default) < ERROR < CRITICAL  
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)

    return logger

log = create_logger('s3_wraper', logging.INFO)

