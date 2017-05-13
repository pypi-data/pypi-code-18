from .Client import Client
from .Helper import Helper


class PersonalClient (Client):

    def personal_import_raw_key(self, keydata, passphrase, raw=True):
        """
        Imports the given unencrypted private key (hex string) into the key store, encrypting it with the passphrase.
        :param keydata: encrypted private key
        :param passphrase: Passphrase to unlock the account
        :param raw:
        :return: Address of the new account
        """
        payload = Helper.generate_empty_payload("personal_importRawKey")
        payload['params'] = [
            keydata,
            passphrase
        ]

        response = self.request(payload)
        return Helper.result_or_raw(raw, response)

    def personal_list_accounts(self, raw=True):
        """
        Returns all the Ethereum account address of all keys in the key store.
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("personal_listAccount")
        payload['params'] = []

        response = self.request(payload)
        return Helper.result_or_raw(raw, response)

    def personal_lock_account(self, address, raw=True):
        """
        Removes the private key with given address from memory. The account can no longer be used to send transactions.
        :param address:
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("personal_lockAccount")
        payload['params'] = [
            address
        ]

        response = self.request(payload)
        return Helper.result_or_raw(raw, response)

    def personal_new_account(self, passphrase, raw=True):
        """
        Generates a new private key and stores it in the key store directory. The key file is
        encrypted with the given passphrase.
        :param passphrase:
        :param raw:
        :return: Address of the new account
        """
        payload = Helper.generate_empty_payload("personal_newAccount")
        payload['params'] = [
            passphrase
        ]

        response = self.request(payload)
        return Helper.result_or_raw(raw, response)

    def personal_unlock_account(self, address, passphrase, duration=300, raw=True):
        """
        Decrypts the key with the given address from the key store.

        The unencrypted key will be held in memory until the unlock duration expires.
        If the unlock duration defaults to 300 seconds. An explicit duration of zero seconds unlocks the key
        until geth exits.

        The account can be used with eth_sign and eth_sendTransaction while it is unlocked.
        :param address:
        :param passphrase:
        :param duration:
        :param raw:
        :return: boolean
        """
        payload = Helper.generate_empty_payload("personal_unlockAccount")
        payload['params'] = [
            address,
            passphrase,
            duration
        ]

        response = self.request(payload)
        return Helper.result_or_raw(raw, response)

    def personal_send_transaction(self, tx, passphrase, raw=True):
        """
        Validate the given passphrase and submit transaction.

        The transaction is the same argument as for eth_sendTransaction and contains the from address.
        If the passphrase can be used to decrypt the private key belogging to tx.from the transaction is verified,
        signed and send onto the network. The account is not unlocked globally in the node and cannot be used in
        other RPC calls.
        :param tx: TX object (see Helper.generate_tx_object)
        :param passphrase:
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("personal_sendTransaction")
        payload['params'] = [
            tx,
            passphrase
        ]

        response = self.request(payload)
        return Helper.result_or_raw(raw, response)

    def personal_sign(self, message, account, passphrase, raw=True):
        """
        Sign a message with the provided account and passphrase to unlock the account
        :param message:
        :param account:
        :param passphrase:
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("personal_sign")
        payload['params'] = [
            message,
            account,
            passphrase
        ]

        response = self.request(payload)
        return Helper.result_or_raw(raw, response)


