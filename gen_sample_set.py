__author__ = 'rhunter'
import sys
sys.path.append('../Backend')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'censio.settings'

from backend.models import PhoneDriveData, PhoneGroup, PhoneGroupMembership, PhoneId, DriveData
from survey import models
import datetime
from django.core import serializers

model_list = list()

def main():
    '''
    I want: 2 days of data from phone drive and server drive extraction.
    Retrieve all relevant PhoneIDs
    get all phone groups and memberships
    :return:
    '''
    global model_list
    phone_group = PhoneGroup.objects.all()
    append_dataset(phone_group)
    append_dataset(PhoneGroupMembership.objects.all())
    append_dataset(PhoneId.objects.all())

    append_dataset(PhoneDriveData.objects.filter(start_time__gte=datetime.datetime.utcnow()-datetime.timedelta(days=2)).all())
    append_dataset(DriveData.objects.filter(start_time__gte=datetime.datetime.utcnow()-datetime.timedelta(days=2)).all())

    with open('data_dump.json', 'w') as out:
        serializers.serialize('json', model_list, stream=out)

def append_dataset(query_set):
    global model_list
    if len(query_set) > 0:
	if len(model_list) > 0:
            model_list += list(query_set)
	else:
	    model_list = list(query_set)


if __name__ == "__main__":
    main()
