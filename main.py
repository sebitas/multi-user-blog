# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import webapp2
import jinja2
import codecs
import re

from classes.handler import Handler
from classes.welcome import Welcome
from classes.blog import *
from classes.post import *
from classes.sign import *

app = webapp2.WSGIApplication([('/blog/newpost', NewPost),
                               ('/welcome', Welcome),
                               ('/blog', Blog),
                               (r'/blog/(\d+)', PostHandler),
                               ('/signup', SignUp),
                               ],
                            debug=True)


