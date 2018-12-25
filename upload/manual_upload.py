from .app import dicomdb

import dicom
import glob


def test_upload():
    dcm_input_dir = "/home/rsmith/radiation_therapy/test/ANON0/"
    patientName = "ANON12155"
    user_id = 1

    dcm_files = glob.glob(dcm_input_dir + '/*.dcm')
    for dcm_file in dcm_files:
        if dcm_file:
            dcm = dicom.read_file(dcm_file)
            res = dicomdb.parse(dcm, user_id)

            if res:
                print("{0} completed".format(dcm))
                continue
            else:
                print("{0} did not load".format(dcm))
            