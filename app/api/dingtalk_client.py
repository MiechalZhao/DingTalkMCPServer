from app.utils.logger import setup_logger
import logging
import json
import dingtalk_stream
from dingtalk_stream import AckMessage
from app.core.message_service import MessageService

class DingTalkClient(dingtalk_stream.GraphHandler):
    def __init__(self,logger : logging.Logger = None):
        super(dingtalk_stream.GraphHandler, self).__init__()
        super().__init__()
        if logger:
            self.logger = logger

    async def process(self, callback: dingtalk_stream.CallbackMessage):
        request = dingtalk_stream.GraphRequest.from_dict(callback.data)
        self.logger.info('incoming request, method = %s', request.request_line.method)
        process_result = MessageService.process_message(request.request_line.method)
        response = dingtalk_stream.GraphResponse()
        response.status_line.code = 200
        response.status_line.reason_phrase = 'OK'
        response.headers['Content-Type'] = 'application/json'

        response.body = json.dumps({
            'name': process_result.get('name'),
            'dateStr': process_result.get('date'),
            'text': process_result.get('text'),
            'team_info': process_result.get('team_info')
        }, ensure_ascii=False)
        return AckMessage.STATUS_OK, response.to_dict()
