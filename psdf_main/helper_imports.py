from django.shortcuts import render, redirect
from django.http import HttpResponse, request, HttpResponseRedirect
from .forms import *
from .helpers import *
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
import os
import mimetypes
from pathlib import Path
import shutil
from werkzeug.utils import secure_filename
import glob




BASE_DIR = Path(__file__).resolve().parent.parent