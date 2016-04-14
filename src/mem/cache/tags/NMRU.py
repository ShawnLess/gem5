"""
Tags with Not Most Recently Used Policy
Author: shawnless.xie@gmail.com

"""

from Tags import BaseSetAssoc

class NMRU(BaseSetAssoc):
    type        ='NMRU'
    cxx_header  ="mem/cache/tags/nmru.hh"
