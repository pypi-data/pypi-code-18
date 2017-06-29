from .AccountAsset import AccountAsset
from .AccountAssetTypes import AccountAssetTypes
from .AccountBalance import AccountBalance
from .AccountList import AccountList
from .Address import Address
from .BankAsset import BankAsset
from .BankList import BankList
from .CreateAccountReqBody import CreateAccountReqBody
from .CreateBankReqBody import CreateBankReqBody
from .CreateCreditCardReqBody import CreateCreditCardReqBody
from .CreateProfileReqBody import CreateProfileReqBody
from .CreditCardAsset import CreditCardAsset
from .CreditCardList import CreditCardList
from .DeactivateUserReqBody import DeactivateUserReqBody
from .Debit import Debit
from .Email import Email
from .EmailDetails import EmailDetails
from .EmailDetailsTypes import EmailDetailsTypes
from .EmailList import EmailList
from .KYC import KYC
from .KYCDocument import KYCDocument
from .KYCDocumentList import KYCDocumentList
from .KYCStatuses import KYCStatuses
from .KYCTypes import KYCTypes
from .MeProfile import MeProfile
from .Phone import Phone
from .PhoneList import PhoneList
from .PhoneNumberTypes import PhoneNumberTypes
from .Profile import Profile
from .Transaction import Transaction
from .TransactionDetails import TransactionDetails
from .TransactionList import TransactionList
from .TransactionReasons import TransactionReasons
from .TransactionStatuses import TransactionStatuses
from .VerifyBankReqBody import VerifyBankReqBody
from .VerifyProfileReqBody import VerifyProfileReqBody
from .Work import Work

from .client import Client as APIClient

from .oauth2_client_oauth_2_0 import Oauth2ClientOauth_2_0

__version__ = '0.0.9'


class Client(object):
    def __init__(self, base_uri="https://sandbox.paycash.eu/paycash-server/v3/api"):
        self.api = APIClient(base_uri)

        self.oauth2_client_oauth_2_0 = Oauth2ClientOauth_2_0(self.api)
