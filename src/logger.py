import logging 


def setup_logger(level = "INFO"):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s"
        
    )
    
    return logging.getLogger()


