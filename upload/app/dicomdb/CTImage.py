from upload.models import CTImages
from django.core.exceptions import ObjectDoesNotExist
import sys
import numpy as np

def parse(dcm, user, patient, study, series):
    try:
        Image = CTImages.objects.get(SOPInstanceUID=dcm.SOPInstanceUID)
    except ObjectDoesNotExist:
        Image = CTImages()
        Image.SOPInstanceUID = dcm.SOPInstanceUID
        Image.SOPClassUID = dcm.SOPClassUID
        Image.ImageType = dcm.ImageType
        Image.PhotometricInterpretation = dcm.PhotometricInterpretation if "PhotometricInterpretation" in dcm and dcm.PhotometricInterpretation else None
        Image.RescaleSlope = dcm.RescaleSlope
        Image.RescaleIntercept = dcm.RescaleIntercept
        Image.SliceLocation = dcm.SliceLocation
        Image.PixelSpacing = ','.join([str(point) for point in np.array(dcm.PixelSpacing)])
        Image.ImageOrientationPatient = ','.join([str(point) for point in np.array(dcm.ImageOrientationPatient)])
        Image.ImagePositionPatient = ','.join([str(point) for point in np.array(dcm.ImagePositionPatient)])
        Image.SliceThickness = dcm.SliceThickness
        Image.BodypartExamined = dcm.BodyPartExamined if "BodyPartExamined" in dcm and dcm.BodyPartExamined else None
        Image.Rows = dcm.Rows
        Image.Columns = dcm.Columns
        Image.fk_series_id = series
        Image.fk_study_id = study
        Image.fk_patient_id = patient
        Image.fk_user_id = user
    try:
        Image.save()
    except:
        print(sys.exc_info())
        return False

    return True
