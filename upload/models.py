# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import dicom

# Create your models here.
class Patient(models.Model):
    class Meta:
        db_table = 'patients'
    PatientName = models.CharField(max_length=200)
    BirthDate = models.DateField(null=True)
    Gender = models.CharField(max_length=20,null=True)
    EnthicGroup = models.CharField(max_length=200,null=True)
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Study(models.Model):
    class Meta:
        db_table = 'studies'
    StudyInstanceUID = models.CharField(max_length=200)
    StudyDate = models.DateField(null=True)
    StudyDescription = models.CharField(max_length=200,null=True)
    TotalSeries = models.IntegerField()
    fk_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Series(models.Model):
    class Meta:
        db_table = 'series'
    SeriesInstanceUID = models.CharField(max_length=200)
    SeriesDate = models.DateField(null=True)
    SeriesDescription = models.CharField(max_length=200,null=True)
    SeriesType = models.CharField(max_length=100)
    Modality = models.CharField(max_length=100)
    SeriesNumber = models.CharField(max_length=100,null=True)
    PhysicianOfRecord = models.CharField(max_length=100,null=True)
    Manufacturer = models.CharField(max_length=50,null=True)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)
    fk_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class CTImages(models.Model):
    class Meta:
        db_table = 'ct_images'
    SOPInstanceUID = models.CharField(max_length=200)
    SOPClassUID = models.CharField(max_length=100)
    ImageType = models.CharField(max_length=100)
    PhotometricInterpretation = models.CharField(max_length=20,null=True)
    RescaleSlope = models.IntegerField()
    RescaleIntercept = models.IntegerField()
    SliceLocation = models.IntegerField()
    PixelSpacing = models.CharField(max_length=50)
    ImageOrientationPatient = models.CharField(max_length=100)
    ImagePositionPatient = models.CharField(max_length=100)
    SliceThickness = models.CharField(max_length=100)
    BodypartExamined = models.CharField(max_length=100,null=True)
    Rows = models.IntegerField()
    Columns = models.IntegerField()
    fk_series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)
    fk_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class RTStructureSet(models.Model):
    class Meta:
        db_table = 'rt_structureset'
    SOPInstanceUID = models.CharField(max_length=200)
    SOPClassUID = models.CharField(max_length=100)
    TotalROIs = models.IntegerField()
    fk_series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)
    fk_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class ROI(models.Model):
    class Meta:
        db_table = 'oar_dictionary'
    ROIName = models.CharField(max_length=100,unique=True)
    ROIDisplayColor = models.CharField(max_length=100)

class RTROI(models.Model):
    class Meta:
        db_table = 'rt_rois'
    ROIName = models.CharField(max_length=100)
    Volume = models.FloatField()
    TotalContours = models.IntegerField()
    ROINumber = models.CharField(max_length=200,null=True)
    fk_structureset_id = models.ForeignKey(RTStructureSet, on_delete=models.CASCADE)
    fk_series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)
    fk_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class RTContour(models.Model):
    class Meta:
        db_table = 'rt_contour'
    ContourGeometricType = models.CharField(max_length=100)
    NumberOfContourPoints = models.IntegerField()
    ContourData = models.TextField()
    ReferencedSOPClassUID = models.CharField(max_length=100)
    ReferencedSOPInstanceUID = models.CharField(max_length=100)
    fk_roi_id = models.ForeignKey(RTROI, on_delete=models.CASCADE)
    fk_structureset_id = models.ForeignKey(RTStructureSet, on_delete=models.CASCADE)

class RTDose(models.Model):
    class Meta:
        db_table = 'rt_dose'
    SOPClassUID = models.CharField(max_length=100)
    SOPInstanceUID = models.CharField(max_length=100)
    DoseGridScaling = models.CharField(max_length=100)
    DoseSummationType = models.CharField(max_length=100,null=True)
    DoseType = models.CharField(max_length=100,null=True)
    DoseUnits = models.CharField(max_length=100,null=True)
    ReferencedRTPlanSequence = models.CharField(max_length=100)
    ReferencedStructureSetSequence = models.CharField(max_length=100)
    fk_series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)
    fk_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class RTDoseImage(models.Model):
    class Meta:
        db_table = 'rt_dose_image'
    Columns = models.IntegerField()
    Rows = models.IntegerField()
    ImageOrientationPatient = models.CharField(max_length=20)
    ImagePositionPatient = models.CharField(max_length=20)
    PhotometricInterpretation = models.CharField(max_length=20,null=True)
    PixelSpacing = models.CharField(max_length=20)
    NumberOfFrames = models.IntegerField()
    ImageData = models.TextField()
    fk_dose_id = models.ForeignKey(RTDose, on_delete=models.CASCADE)
    fk_series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)
    fk_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class RTDVH(models.Model):
    class Meta:
        db_table = 'rt_dvh'
    DVHDoseScaling = models.CharField(max_length=20)
    DVHMaximumDose = models.FloatField()
    DVHMeanDose = models.FloatField()
    DVHMinimumDose = models.FloatField()
    DVHNumberOfBins = models.IntegerField()
    DVHReferencedROI = models.CharField(max_length=10)
    DVHType = models.CharField(max_length=10,null=True)
    DVHVolumeUnits = models.CharField(max_length=10)
    DoseType = models.CharField(max_length=10)
    DoseUnits = models.CharField(max_length=10)
    DVHData = models.TextField()
    fk_dose_id = models.ForeignKey(RTDose, on_delete=models.CASCADE)
    fk_series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)
    fk_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class RTIsDose(models.Model):
    class Meta:
        db_table = 'rt_isdose'

    RowPosition = models.TextField()
    ColumnPosition = models.TextField()
    IsDoseValue = models.IntegerField()
    fk_ct_image_id = models.ForeignKey(CTImages, on_delete=models.CASCADE)
    fk_dose_id = models.ForeignKey(RTDose, on_delete=models.CASCADE)
    fk_series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)
    fk_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)

class RTGeneralPlan(models.Model):
    class Meta:
        db_table = 'rt_general_plan'
    planLabel = models.TextField()
    planName = models.TextField(null=True)    
        
class OVH(models.Model):
    class Meta:
        db_table = 'ovh'

    binValue = models.TextField(null=True)
    binAmount = models.TextField(null=True)
    OverlapArea = models.IntegerField(null=True)
    #to specify the ptv_id and oar_id for ovh
    ptv_id = models.IntegerField(null=True)
    OAR_id = models.IntegerField(null=True)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)


#a Model to store sts
class STS(models.Model):
    class Meta:
        db_table = 'sts'

    elevation_bins = models.TextField(null=True)
    distance_bins = models.TextField(null=True)
    azimuth_bins = models.TextField(null=True)
    amounts = models.TextField(null=True)
    #to specify which ptv and which oar
    ptv_id = models.IntegerField(null=True)
    OAR_id = models.IntegerField(null=True)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)

class Similarity(models.Model):
    class Meta:
        db_table = 'similarity'
    DBStudyID = models.CharField(max_length=100)
    Similarity = models.FloatField(max_length=200)
    OVHDisimilarity = models.FloatField(max_length=200)
    STSDisimilarity = models.FloatField(max_length=200)
    TargetOAR = models.CharField(max_length=200)
    fk_study_id = models.ForeignKey(Study, on_delete=models.CASCADE)
