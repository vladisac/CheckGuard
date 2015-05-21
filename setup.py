'''
 *  Copyright (C) 2015 Touch Vectron
 *
 *  Author: Cornel Punga
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License version 2 as
 *  published by the Free Software Foundation.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *  MA 02110-1301, USA.
 *
 *	Filename: setup.py
 *	This module is used to track dependencies and compile source
 *      using py2exe
 *
 *      Usage:  python setup.py py2exe
 *              Two directories will be created when you run your setup
 *              script, build and dist. The build directory is used as working
 *              space while your application is being packaged.
 *              It is safe to delete the build directory after your setup script
 *              has finished running. The files in the dist directory are the
 *              ones needed to run your application.
 *
 *	Last revision: 05/21/2015
 *
'''

from distutils.core import setup
try:
    import py2exe
except ImportError:
    print("You must have py2exe module installed")
    exit()

setup(console=['CheckGuard.py'], requires=['watchdog', 'py2exe'])
