import requests
import sys
import json
import random
from kapacitor.udf.agent import Agent, Handler
from kapacitor.udf import udf_pb2

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()


# Verifies the registration of an event with Crypotwerk
# using the retrievalId
#
class BlockchainHandler(Handler):

    def __init__(self, agent):
        self._agent = agent
        self._retrievalId = None

    def info(self):
        response = udf_pb2.Response()
        response.info.wants = udf_pb2.STREAM
        response.info.provides = udf_pb2.STREAM
        #response.info.options['retrievalId'].valueTypes.append(udf_pb2.STRING)

        return response

    def init(self, init_req):
        success = True
        msg = ''
        for opt in init_req.options:
            if opt.name == 'retrievalId':
                self._retrievalId = opt.values[0].stringValue

        if self._retrievalId is None:
            success = False
            msg += ' must supply valid retrievalId'

        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]

        return response

    def checkBlockchain(self, idreg):

        apiUrl = 'https://developers.cryptowerk.com/platform/API/v6/verify'

        headers = {
            'Accept': 'application/json',
            'X-API-Key': 'URsuROac/Qb4WD9g14k9Vi6vFaV+B0mkNEZrcRAltsg= 32lWe9BTEwfF0ThAkp2QplwXN2Qq74ICsxSu9H3MdJs='
        }
        #try:
            #r = requests.post(apiUrl, params={'version': '6', 'retrievalId': idreg}, headers = headers)
        #except Exception as e:
        #    success = False
        #    msg = "Error verifing Cryptowerk registration"

       #Sample data randomizer

        generalName = ['Bitcoin', 'Ethereum', 'Ripple']
        hasBeenInsertedIntoAtLeastOneBlockchain = ['true', 'false']

       #Sample Cryptowerk json response onject // used for testing - see  RT request example above
        b = ({
            "minSupportedAPIVersion": 1,
            "documents": [
                {
                    "submittedAt": 1545849139472,
                    "name": "flux0",
                    "hasBeenInsertedIntoAllRequestedBlockchains": "true",
                    "hasBeenInsertedIntoAtLeastOneBlockchain": random.choice(hasBeenInsertedIntoAtLeastOneBlockchain),
                    "retrievalId": "ri0000000000000000000000000000000000000000000000000000000000000",
                    "sealsAreComplete": "true",
                    "seals": [
                        {
                            "operations": [
                                {
                                    "submittedAt": 1545849139472,
                                    "opcode": "DOCUMENTINFO",
                                    "name": "flux0"
                                    },
                                {
                                    "blockChainId": "cc88a7ad1b3033fd3e4135e9ec5317dbd4fdc24e72a8018ed42fd3f355241fab",
                                    "instanceName": "MyTest",
                                    "opcode": "BLOCKCHAIN",
                                    "blockchainGeneralName": "Bitcoin",
                                    "insertedIntoBlockchainAt": 1545849753242
                                },
                                {
                                    "docHash": "71e4af6d3a605cf0a94666a03c0f6f9771700e3257281e2b85f09a2880c97df4",
                                    "opcode": "DOC_SHA256"
                                },
                                {
                                    "hash": "9c81d330a82cc58dafdab97093d841f5fa8f92d77eac54d0f1a23b22c2d187a3",
                                    "opcode": "APPEND_THEN_SHA256"
                                },
                                {
                                    "hash": "6320d917a7f53e68af0a0ffd694bcdcd8503536b704062426f6ddfd93ea8a75f",
                                    "opcode": "APPEND_THEN_SHA256"
                                },
                                {
                                    "hash": "a16bfff35f94df6e707c00cc01bde86392d0360264aa39ac16315a40fac665c6",
                                    "opcode": "ANCHOR_SHA256"
                                }
                            ],
                            "version": 7,
                            "bundleMethod": "BALANCED_MERKLE_TREE"
                            },
                            {
                            "operations": [
                                {
                                    "submittedAt": 1545849139472,
                                    "opcode": "DOCUMENTINFO",
                                    "name": "flux0"
                                },
                                {
                                    "blockChainId": "0xc504873544a48c6b3dd846dd3dc8b37760ba51335cb80e714e5e20fea9205f80",
                                    "instanceName": "4",
                                    "opcode": "BLOCKCHAIN",
                                    "blockchainGeneralName": "Ethereum",
                                    "insertedIntoBlockchainAt": 1545849171610
                                },
                                {
                                    "docHash": "71e4af6d3a605cf0a94666a03c0f6f9771700e3257281e2b85f09a2880c97df4",
                                    "opcode": "DOC_SHA256"
                                },
                                {
                                    "hash": "71e4af6d3a605cf0a94666a03c0f6f9771700e3257281e2b85f09a2880c97df4",
                                    "opcode": "ANCHOR_SHA256"
                                }
                            ],
                            "version": 7,
                            "bundleMethod": "BALANCED_MERKLE_TREE"
                            }
                        ],
                        "blockchainRegistrations": [
                            {
                                "status": {

                            },
                                "blockChainId": "cc88a7ad1b3033fd3e4135e9ec5317dbd4fdc24e72a8018ed42fd3f355241fab",
                                "blockChainDesc": {
                                    "generalName": random.choice(generalName),
                                    "instanceName": "MyTest"
                            },
                                "insertedIntoBlockchainAt": 1545849753242
                            },
                            {
                                "status": {
                                    "atLeastThisNumberOfConfirmations": 170,
                                    "isConsideredFinal": "true"
                            },
                                "blockChainId": "0xc504873544a48c6b3dd846dd3dc8b37760ba51335cb80e714e5e20fea9205f80",
                                "blockChainDesc": {
                                    "generalName": "Ethereum",
                                    "instanceName": "4"
                            },
                                "insertedIntoBlockchainAt": 1545849171610
                            }
                        ]
                    }
                ],
                "maxSupportedAPIVersion": 6
            })
        return b

    def snapshot(self):

        response = udf_pb2.Response()
        response.snapshot.snapshot = ''
        return response

    def restore(self, restore_req):

        response = udf_pb2.Response()
        response.restore.success = False
        response.restore.error = 'not implemented'
        return response

    def begin_batch(self, begin_req):
        raise Exception("not supported")

    def point(self, point):

        response = udf_pb2.Response()
        response.point.CopyFrom(point)

        idreg = point.fieldsDouble[self._retrievalId]

        logger.debug('Verifing blockchain registration for _retrievalId: ' +str(idreg))

        # Check against the Cryptowerk api for event registration
        data = self.checkBlockchain(idreg)

        response.point.fieldsString["submittedAt"] = str(data["documents"][0]["submittedAt"])
        response.point.fieldsString["hasBeenInsertedIntoAtLeastOneBlockchain"] = str(data["documents"][0]["hasBeenInsertedIntoAtLeastOneBlockchain"])

        if str(data["documents"][0]["hasBeenInsertedIntoAtLeastOneBlockchain"]) == 'true':
            response.point.fieldsString["nameOfBlockchain"] = str(data["documents"][0]["blockchainRegistrations"][0]["blockChainDesc"]["generalName"])
            response.point.fieldsString["insertedIntoBlockchainAt"] = str(data["documents"][0]["blockchainRegistrations"][0]["insertedIntoBlockchainAt"])
        else:
            logger.debug('Crypotwerk seals not complete for retrievalId: ' +str(idreg))

        self._agent.write_response(response)

        #logger.debug('formed response:'+response.__str__())

    def end_batch(self, end_req):
        raise Exception("not supported")


if __name__ == '__main__':
    a = Agent()
    h = BlockchainHandler(a)
    a.handler = h

    logger.info("Starting Cryptowerk Agent")
    a.start()
    a.wait()
    logger.info("Cryptowerk Agent finished")
