import os
os.environ["DJANGO_SETTINGS_MODULE"] = './../../../dsrt/settings.py'
from upload.models import Patient, Study, Series
from . import CTImage, RTPlan, RTDose, RTStructureset
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth.models import User
type_dict = {
    'RTSTRUCT': RTStructureset,
    'RTDOSE': RTDose,
    'RTPLAN': RTPlan,
    'CT'    : CTImage
}
def parse(dcm,user_id):
    # create the entries into the patients, studies, and studies tables
    # then perform the specifics for the 4 individual types of files
    
    user = User.objects.get(pk = user_id)
    try:
        patient = Patient.objects.get(PatientName = dcm.PatientName)
    except ObjectDoesNotExist:
        print("Creating new patient")
        patient = Patient()
        patient.PatientName = str(dcm.PatientName)
        patient.BirthDate = datetime.datetime.strptime(dcm.PatientBirthDate, "%Y%m%d").date() if ("PatientBirthDate" in dcm) and dcm.PatientBirthDate else None
        patient.Gender = str(dcm.PatientSex) if "PatientSex" in dcm else None
        patient.EnthicGroup = str(dcm.EthnicGroup) if "EthnicGroup" in dcm else None
        patient.fk_user_id = user
        patient.save()
        
    try:
        study = Study.objects.get(StudyInstanceUID = dcm.StudyInstanceUID)
    except ObjectDoesNotExist:
        print("Creating new study")
        study = Study()
        study.StudyInstanceUID = dcm.StudyInstanceUID
        study.StudyDate = datetime.datetime.strptime(dcm.StudyDate, "%Y%m%d").date() if ("StudyDate" in dcm) and dcm.StudyDate else None
        study.StudyDescription = str(dcm.StudyDescription) if "StudyDescription" in dcm else None
        study.TotalSeries = 0
        study.fk_patient_id = patient
        study.fk_user_id = user
        study.save()

    try:
        series = Series.objects.get(SeriesInstanceUID = dcm.SeriesInstanceUID)
    except ObjectDoesNotExist:
        print("Creating new series")
        series = Series()
        series.SeriesInstanceUID = dcm.SeriesInstanceUID
        # series.SeriesDate = datetime.datetime.strptime(dcm.Revi    ewDate,"%Y%m%d").date()
        series.SeriesDescription = str(dcm.SeriesDescription) if "SeriesDescription" in dcm else None
        series.SeriesType = dcm.Modality
        series.Modality = dcm.Modality
        series.SeriesNumber = dcm.SeriesNumber
        series.PhysicianOfRecord = str(dcm.PhysiciansOfRecord) if "PhysiciansOfRecord" in dcm else None
        series.Manufacturer = str(dcm.Manufacturer) if "Manufacturer" in dcm else None
        series.fk_study_id = study
        series.fk_patient_id = patient
        series.fk_user_id = user
        series.save()

    res = type_dict[dcm.Modality].parse(dcm,user,patient,study,series)
    return res
