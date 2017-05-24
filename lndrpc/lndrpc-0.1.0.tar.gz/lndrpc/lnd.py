from __future__ import print_function

import grpc
import lndrpc.rpc_pb2 as rpc_pb2
import lndrpc.rpc_pb2_grpc as rpc_pb2_grpc


def get_lnrpc_client(address):
    channel = grpc.insecure_channel(address)
    client = rpc_pb2_grpc.LightningStub(channel)
    return client


class Lnd:
    def __init__(self, address, *args):
        self.client = get_lnrpc_client(address)

    def get_info(self):
        request = rpc_pb2.GetInfoRequest()
        response = self.client.GetInfo(request)

        return response

    def list_payments(self):
        request = rpc_pb2.ListPaymentsRequest()
        response = self.client.ListPayments(request)

        return response

    def list_invoices(self):
        request = rpc_pb2.ListInvoiceRequest()
        response = self.client.ListInvoices(request)

        return response

    def list_transactions(self):
        request = rpc_pb2.GetTransactionsRequest()
        response = self.client.GetTransactions(request)

        return response

    def subscribe_invoices(self):
        request = rpc_pb2.InvoiceSubscription()
        response = self.client.SubscribeInvoices(request)

        return response

    def subscribe_transactions(self):
        request = rpc_pb2.GetTransactionsRequest()
        response = self.client.SubscribeTransactions(request)

        return response
