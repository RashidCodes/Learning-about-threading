#!/usr/bin/env python


import threading
import logging


class Pipeline:

    def __init__(self):
        self.message = 0;

        # remember that only one thread can have access to a lock at a time
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()

        # the consumer acquires a lock first 
        self.consumer_lock.acquire()


    def get_message(self, name):
        logging.debug("%s:about to acquire getlock", name)
        self.consumer_lock.acquire()
        logging.debug("%s:have getlock", name)
        message = self.message
        logging.debug("%s:about to release setlock", name)
        self.producer_lock.release()
        logging.debug("%s:setlock released", name)
        return message


    
    def set_message(self, message, name):
        logging.debug("%s:about to acquire setlock", name)
        self.producer_lock.acquire()
        logging.debug("%s:have setlock", name)
        self.message = message 
        logging.debug("%s:about to release getlock", name)
        self.consumer_lock.release()
        logging.debug("%s:getlock released", name)




