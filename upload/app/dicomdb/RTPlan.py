import sys

from django.core.exceptions import ObjectDoesNotExist
import numpy as np
from . import utils
from upload.models import RTGeneralPlan


def parse(dcm, user, patient, study, series):
    try:
        generalPlan = RTGeneralPlan.objects.get(SOPInstanceUID=dcm.SOPInstanceUID)
    except ObjectDoesNotExist:
        generalPlan = RTGeneralPlan()
        # PUT IN THE REAL KEYWORDS
        generalPlan.planLabel = dcm.RTPlanLabel
        generalPlan.planName = dcm.RTPlanName
        
    try:
        generalPlan.save()
    except:
        print(sys.exc_info())
        return False

    return True
