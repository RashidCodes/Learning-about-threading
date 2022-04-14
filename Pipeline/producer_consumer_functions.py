#!/usr/bin/env python


import random
import logging

SENTINEL = object();


def producer(pipeline):
    """Getting a message from the network"""
    for index in range(10):
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")


    # Send a sentinel message to tell consumer we're done
    pipeline.set_message(SENTINEL, "Producer")



def consumer(pipeline):
        """Pretend we're saving a number in the database"""
        message = 0

        while message is not SENTINEL:
            message = pipeline.get_message("Consumer")
            if message is not SENTINEL:
                logging.info("Consumer storing message: %s", message)




