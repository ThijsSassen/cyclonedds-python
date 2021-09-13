"""
 * Copyright(c) 2021 ADLINK Technology Limited and others
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v. 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0, or the Eclipse Distribution License
 * v. 1.0 which is available at
 * http://www.eclipse.org/org/documents/edl-v10.php.
 *
 * SPDX-License-Identifier: EPL-2.0 OR BSD-3-Clause


This tool is used in wheels to perform the idlc command.
The idlc binary is under cyclonedds/.bin/idlc, libs are under
cyclonedds/.libs.
"""

import os
import sys
import platform
import subprocess
import cyclonedds

basedir = os.path.abspath(os.path.dirname(cyclonedds.__file__))
idlc = os.path.join(basedir, ".bin", "idlc")
if platform.system() == "Windows":
    idlc += ".exe"

libdir = os.path.join(basedir, ".libs")


def command():
    if not os.path.exists(idlc):
        print("Python idlc entrypoint active but cyclonedds-python installation does not include idlc executable!")
        sys.exit(1)

    environ = os.environ.copy()

    if platform.system() == "Windows":
        environ["PATH"] = ";".join([libdir] + environ.get("PATH", "").split(";"))
    elif platform.system() == "Darwin":
        environ["DYLD_LIBRARY_PATH"] = ":".join([libdir] + environ.get("DYLD_LIBRARY_PATH", "").split(":"))
    else:
        environ["LD_LIBRARY_PATH"] = ":".join([libdir] + environ.get("LD_LIBRARY_PATH", "").split(":"))

    os.execvpe(idlc, sys.argv[1:], environ)