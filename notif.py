# Send an alarm notification from the SnoozeBud to a single mobile device.

from pyfcm import FCMNotification

def send_notif(fcm_id):
    push_service = FCMNotification(api_key="AAAAwRZlYTI:APA91bHQgK_VAcSsVqPD5EpNKVWDfdcPn8XWyZ1XI_N24-AK2Zmh8lPnqjtMfnNBSkYwAooczp8ZuhUIg6UpH7Wb9YXCrfj7WPXCHpKnMcgyQTNxDREXWQX8U2EF70BxYh6MGOs_6R9G")

    data_message = {
            "type": "alarm"
    }

    extra_kwargs = {
        'priority': 'high'
    }

    #registration_id = "eHvMI7WIYAc:APA91bEGCVaNcG2gyccK44NnfLz8q7Rttd7EuOH-G6vLglhadd5wkWcelv5pMIoFF9UqNUlcfI6b8fzyXftLiKEwmCl2LUhUUiHeFwhhnlVp7LkmFEHineuCpOu2J9t2mIEGPAOvTtqT"
    message_title = "Alarm"
    message_body = "A lapse in breathing has been detected..."
    result = push_service.notify_single_device(registration_id=fcm_id, data_message=data_message, extra_kwargs=extra_kwargs)
    #, data_message=data_message

    print result
