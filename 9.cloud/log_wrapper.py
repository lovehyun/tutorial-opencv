import logging

# Logging
def create_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)

    if len(logger.handlers) > 0:
        return logger

    # DEBUG < INFO < WARNING(default) < ERROR < CRITICAL  
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s | %(message)s', datefmt="%Y-%m-%d_%H:%M:%S")
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)

    return logger

log = create_logger('s3_wrapper')
