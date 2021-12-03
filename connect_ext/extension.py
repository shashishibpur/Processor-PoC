# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Globex Corporation
# All rights reserved.
#
from connect.eaas.extension import (
    Extension,
    ProcessingResponse,
    ScheduledExecutionResponse,
)


class Approvesubs244Extension(Extension):

    def process_asset_purchase_request(self, request):

        request_asset = request['asset']
        update_params_request_body = {'asset': {'params': []}}
        if request_asset['status'] == 'processing':
            for param in request_asset['params']:
                self.logger.warning(f" param id is {param['id']}, phase {param['phase']}, required {param['constraints']['required']}, value {param['value']}")
                if param['phase'] == 'fulfillment' and param['constraints']['required'] and not param['value']:
                    update_params_request_body['asset']['params'].append({"id": param['id'], "value": "updateParamValue"})

            if len(update_params_request_body['asset']['params']) > 0:
                self.client.requests[request['id']].put(
                    update_params_request_body
                )
            product_id = request['asset']['product']['id']
            template = self.client.products[product_id]('templates?scope=asset&type=fulfillment').get()
            self.client.requests[request['id']]('approve').post(
                {
                    'template_id': template[0]['id']
                }
            )
            self.logger.warning(f"Approved request {request['id']}")
            self.logger.warning("completed process_asset_purchase_request")
            return ProcessingResponse.done()
        else:
            self.logger.warning(f"request status {request['status']}")
            self.logger.warning(f"{request['status']} subscription is not processed.")

