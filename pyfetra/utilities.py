#==============================================================================
# Copyright (C) 2018 Marchand Basile
# 
# This file is part of pyfetra.
# 
# pyfetra is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# pyfetra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pyfetra.  If not, see <http://www.gnu.org/licenses/>
#==============================================================================

import sys, os
import logging
import code
import time
import __main__ as main

log_code = {"DEBUG" : logging.DEBUG, "INFO" : logging.INFO}




def LOGGER(**kwargs):
    """ pyfetra log file manager

    Function which allows to automatically create log file and display
    more or less several informations on screen

    Parameters 
    ----------
    kwargs : (dict) contain logger option  

    Example 
    -------
    >>> LOGGER(job_id='my_job', display='DEBUG', logfile='DEBUG')
    >>>
    """
    # Declare log level for screen and file
    # Declare logfile =
    module_logger = logging.getLogger("pyfetra")
    module_logger.setLevel(logging.DEBUG)
    if "job_id" in kwargs.keys():
        log_fname = kwargs["job_id"] + ".log"
    else:
        date = "toto"
        log_fname = date.replace(" ","_") + ".log"
    if os.path.exists(log_fname):
        os.remove(log_fname)        
    
    if "display" in kwargs.keys():
        screen = logging.StreamHandler()
        screen.setLevel(log_code[kwargs["display"]])
        module_logger.addHandler(screen)
        formatter_screen = logging.Formatter('pyfetra - %(levelname)-8s :: %(message)s')
        screen.setFormatter(formatter_screen)
    if "logfile" in kwargs.keys():
        log = logging.FileHandler(log_fname)
        log.setLevel(log_code[kwargs["logfile"]])    
        module_logger.addHandler(log)
        formatter_log  = logging.Formatter('%(asctime)-4s :: %(levelname)-8s %(name)-14s :: %(message)s')
        log.setFormatter(formatter_log)

    #f_path = os.path.abspath(main.__file__)
    
    
def __save_job_file(f_path):
    if len(sys.argv) > 1:
        JOB_FILE_CONTENT('Arguments given {}'.format(sys.argv))
    with open(f_path) as f_job:
        f_cont = f_job.read().split('\n')
        for f_line in f_cont:
            JOB_FILE_CONTENT(f_line)


def INTERACT(banner=''):
    ''' Function that mimics octave keyboard command, very usefull for debugging code '''
    # use exception trick to pick up the current frame
    try:
        raise None
    except:
        frame = sys.exc_info()[2].tb_frame.f_back
    module_logger = logging.getLogger("pyToteFEM")
    module_logger.info("INTERACT mode, use quit() to exit : ")
    namespace = frame.f_globals.copy()
    namespace.update(frame.f_locals)
    try:
        code.interact(banner=banner, local=namespace)
    except SystemExit:
        return

def JOB_FILE_CONTENT(msg):
    ''' 
    Function which offers user message and integration in log file

    Paramerters
    -----------
    msg : (str) user message, similar to print input
    
    '''
    module_logger = logging.getLogger("pyfetra")
    logging.JOBFILE = 26
    logging.addLevelName(logging.JOBFILE,'JOB FILE')
    logging.jobfile = lambda msg, *args: module_logger._log(logging.JOBFILE, msg, args)
    logging.jobfile(msg)


def MESSAGE(msg):
    ''' 
    Function which offers user message and integration in log file

    Paramerters
    -----------
    msg : (str) user message, similar to print input
    
    '''
    module_logger = logging.getLogger("pyfetra")
    logging.MESSAGE = 25
    logging.addLevelName(logging.MESSAGE,'MESSAGE')
    logging.message = lambda msg, *args: module_logger._log(logging.MESSAGE, msg, args)
    logging.message(msg)

 
