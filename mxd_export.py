#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script has been created to optimize the time when exporting
        mxd files! 
        author: Daniel Guerrero - dfgm2006@gmail.com
        """

from __future__ import print_function
import argparse
import arcpy
import os
import multiprocessing

parser = argparse.ArgumentParser(description='This script will export the \
                                the mxd files to the desired format, by default is .PDF.')
parser.add_argument('workspace', 
                    help='folder in which are located the mxd files')
parser.add_argument('output_path', 
                    help='folder to store the mxd exported files')
parser.add_argument('-p', '--processes', default=multiprocessing.cpu_count(),
                    help='set the number of processes')

args = parser.parse_args()


def export_to_pdf(workspace, mxd, outh_path):
    current_mxd = arcpy.mapping.MapDocument(os.path.join(workspace, mxd))
    pdf_name = "{}.pdf".format(mxd[:-4])
    out_path_name = os.path.join(out_path, pdf_name)

    if not os.path.exists(out_path_name):
        arcpy.mapping.ExportToPDF(current_mxd, out_path_name)
        print('The pdf file: "{}" has been exported correctly.'.format(pdf_name))
    else:
        print('The pdf file: "{}" already exist...'.format(pdf_name))
    del current_mxd
    return


number_of_process = int(args.processes)
arcpy.env.workspace = ws = args.workspace


out_path = args.output_path
mxd_list = arcpy.ListFiles("*.mxd")


if __name__ == '__main__':
    pool = multiprocessing.Pool(number_of_process)
    for mxd in mxd_list:
        pool.apply_async(export_to_pdf, args=(ws, mxd, out_path,))
    pool.close()
    pool.join()