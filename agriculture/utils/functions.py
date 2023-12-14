import uuid
import re
from rest_framework.response import Response

def genererate_string():
    chaine = str(uuid.uuid4()).replace("-", "")
    grouped_chaine = "-".join(chaine[i:i+4] for i in range(0, len(chaine), 4))

    return grouped_chaine[:30]



def process_phone_number_cg_am(phone):
    patterns = [
        (r'^\+242(\d+)$', lambda x: x[1:]),
        (r'^242(\d+)$', lambda x: x),
        (r'^(05|04)(\d+)$', lambda x: '242' + x)
    ]

    for pattern, action in patterns:
        match = re.match(pattern, phone)
        if match:
            return action(phone)

    return Response({'error':'incorrect phone'})