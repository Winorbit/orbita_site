from django.test import TestCase
from django.core import mail
import uuid
from datetime import datetime
from webui import users

TestCase.MaxDiff = None
# users.datetime_to_token

hours_24 = 86400
hours_25 = 90000
hours_23 = 82800

# now_in_secs = datetime.now().strftime("%s")

now_in_secs = 1592658145
token = "616358702115"
uuid_token = "16fd2706-8baf-433b-82eb-8c7fada847da"

# uuid_token = str(uuid.uuid4())

day_ago =  1592571745  # now_in_secs - hours_24

less_day_ago = 1592575345 # now_in_secs - hours_23

more_day_ago = 1592568145 #  now_in_secs - hours_25


datetime_to_int = 251248200927137534391601

test_email = "Уважаемый Egor вы можете востанвиь доступ к сайту, перейдя о следующей ссылке: localhost/restore_access/1ed38f1a-e714-4a02-afc0-208ec1d7309f/616358702115. Ссылка будет действительна в течении 24 часов."
      

def is_valid_uuid(uuid_to_test:str, version=4):
    """
    Check if uuid_to_test is a valid UUID.
    Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}
    """
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
    pass

class RestoreAccess(TestCase):
    MaxDiff = None
    
    def test_datetime_to_token(self):
        self.assertEqual(users.datetime_to_token(now_in_secs), str(now_in_secs*387))

    def test_token_to_datetime(self):
        self.assertEqual(users.token_to_datetime(token), int(token)/387)
    
    def test_check_expir_token(self):
        fresh_token = users.encode_str_to_number(str(less_day_ago))
        expired_token = users.encode_str_to_number(str(more_day_ago))
        day_to_day_token = users.encode_str_to_number(day_ago) 
        self.assertTrue(users.check_expir_token(now_in_secs, fresh_token))
        self.assertFalse(users.check_expir_token(now_in_secs, expired_token))
        self.assertFalse(users.check_expir_token(now_in_secs, day_to_day_token))
    
    def test_generate_restore_link(self):
        test_email = "testmail@gmail.com"
        test_email_to_int = 9533142343906178599764765337441099194787188
        
        test_user_id = 31
        
        test_datetime = now_in_secs 
        test_datetime_to_int = 251248200927137534391601

        generated_link = users.generate_restore_link(now_in_secs, test_email, test_user_id)
        splited_generated_link = generated_link.split("/")
        self.assertTrue(is_valid_uuid(splited_generated_link[2])) 
        self.assertEqual(int(splited_generated_link[3]), datetime_to_int)
        self.assertEqual(int(splited_generated_link[4]), test_email_to_int)
        self.assertEqual(int(splited_generated_link[5]), test_user_id)
        self.assertEqual(splited_generated_link[1], "restore_access")

    def test_email_generation(self):
        username = "Egor"
        restore_email = users.email_for_restore_access(now_in_secs)
        self.assertEqual(restore_email, test_email)

    def test_send_email(self):
        username = "Egor"
        restore_email = users.email_for_restore_access(now_in_secs)
        email_address = "testmail@gmail.com"
        users.send_restore_message(email_address, restore_email)
        self.assertEqual = (mail.outbox[0].subject, "Password restore")
        self.assertTrue(len(mail.outbox) == 1)

"""

python manage.py test webui.tests.restore_access_test.RestoreAccess.test_check_expir_token

"""
