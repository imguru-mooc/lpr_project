from __future__ import print_function
import pandas as pd
from io import StringIO
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)

from IPython.core import magic_arguments

import tempfile, os, tarfile
import shutil

import docker
import etcd3

# The class MUST call this class decorator at creation time
@magics_class
class EiiMagics(Magics):
    UDF_PATH = '/EIS/go/src/IEdgeInsights/common/udfs/python/'
    VI_CONTAINER = 'ia_video_ingestion'
    VA_CONTAINER = 'ia_video_analytics'

    def _make_tar_file(self, tempdir, directory):
        cwd = os.getcwd()
        os.chdir(tempdir.name)

        tar = tarfile.open(directory + '.tar', mode='w')
        try:
            tar.add(directory)
        finally:
            tar.close()

        os.chdir(cwd)

    def _copy_files(self, files, tempdir, directory):
        cwd = os.getcwd()
        os.chdir(tempdir.name + '/' + directory)
        os.mkdir('ref')

        for f in files:
            shutil.copy(cwd + '/' + f, tempdir.name + '/' + directory + '/ref/')

        os.chdir(cwd)

    def _save_cell(self, cell, tempdir, directory, filename):
        cwd = os.getcwd()
        os.chdir(tempdir.name)
        os.mkdir(directory)

        with open(directory + '/' + filename + '.py', 'w') as f:
            f.write(cell)

        os.chdir(cwd)

    def _print_logs(self, container):
        logs = container.logs(tail=30)
        print(logs.decode())

    def _video_process(self, args, cell, container_name):
        directory = ''
        filename = ''

        # Prepare container object
        dc = docker.from_env()
        container = dc.containers.get(container_name)

        # line parsing
        if 'logs' in args.arg1:
            self._print_logs(container)
            return 'Done'
        elif '.' in args.arg1:
            param = args.arg1.split('.')
            directory = param[0]
            filename = param[1]
        else:
            filename = args.arg1

        tempdir = tempfile.TemporaryDirectory()

        # 1. Save cell to file
        self._save_cell(cell, tempdir, directory, filename)

        # 2. Save IR files
        if len(args.files) > 0:
            self._copy_files(args.files, tempdir, directory)

        # 3. Make tarfile
        self._make_tar_file(tempdir, directory)

        # 2. Copy file to ia_video_ingestion docker image
        print('Copy Udf to container')
        data = open(tempdir.name + '/' + directory + '.tar', 'rb').read()
        container.put_archive(self.UDF_PATH, data)

        # 3. docker restart or etcd configuration update
        print('Restart container...')
        container.restart()

        # 5. Clean up
        tempdir.cleanup()

        return 'Done'

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        'arg1', type=str,
        help='logs | udf class name'
    )
    @magic_arguments.argument(
        'files', nargs='*',
        help='files'
    )
    @line_cell_magic
    def video_ingestion(self, line, cell=None):
        args = magic_arguments.parse_argstring(self.video_ingestion, line)
        return self._video_process(args, cell, self.VI_CONTAINER)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        'arg1', type=str,
        help='logs | udf class name'
    )
    @magic_arguments.argument(
        'files', nargs='*',
        help='files'
    )
    @line_cell_magic
    def video_analytics(self, line, cell=None):
        args = magic_arguments.parse_argstring(self.video_analytics, line)
        return self._video_process(args, cell, self.VA_CONTAINER)
 
    @line_cell_magic
    def etcd(self, line, cell=None):
        # etcd = etcd3.client(host='127.0.0.1', port=2379)
        # etcd.get('/VideoIngestion/config')
        # etcd.close()
        pass

 
ipy = get_ipython()
ipy.register_magics(EiiMagics)

