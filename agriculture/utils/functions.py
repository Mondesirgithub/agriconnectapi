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




def cg_am_transaction_message(status):
    status_messages = {
        "200": {"message": "Transaction successful"},
        "0": {"error": {"message": "Transaction aborted or unfinished"}},
        "60019": {"error": {"message": "Insuficient fund at client end"}},
        "60011": {"error": {"message": "Sender has reached your maximum count of transactions for the day"}},
        "60014": {"error": {"message": "Sender has reached your maximum transaction amount for the day."}},
        "00068": {"error": {"message": "PIN or validation code is wrong"}},
        "01035": {"error": {"message": "Internet connection or service timed out"}},
        "00017": {"error": {"message": "Client has entered a PIN too long than 4 digits"}},
        "01056": {"error": {"message": "Re-imbursement of a client has been rejected"}},
        "00409": {"error": { "message": "entered amount is less for this transaction"}},
        "00099": {"error": {"message": "if the next PIN is wrong your account will be locked"}},
        "10001": {"error": {"message": "destination MSISDN doesn't have an airtel Money account"}},
        "00084": {"error": {"message": "No product type or service is defined for this transaction"}},
        "00332": {"error": { "message": "client's PIN is not numeric"}},
        "00359": {"error": { "message": "Client account is unblocked and the default password is 1234"}},
        "00030": {"error": {"message": "Requested amount is less than the minimum allowed by the platform"}},
        "99046": {"error": {"message": "Entered amount is less than the one requested for this transaction"}},
        "00043": {"error": {"message": "Transaction amount is higher than the maximum allowed"}},
        "400": {"error": {"message": "Transaction was not found in the receiving country"}},
        "404": {"error": {"message": "Application interface not found"}},
        "410": {"error": {"message": "Transaction amount is more than the allowed value."}},
        "450": {"error": {"message": "Transaction not found in the switch"}},
        "250": {"error": {"message": "Undefined response received from destination country"}},
        "MER_404": {"error": {"code": "MER_404", "message": "E-merchant profile not found or incorrect"}}
    }


    return status_messages.get(status, {})