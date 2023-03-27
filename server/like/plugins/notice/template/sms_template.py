from like.utils.tools import ToolsUtil


class SmsTemplate(object):

    def __init__(self, sms_type, sms_notice):
        self.sms_type = sms_type
        config = ToolsUtil.json_to_map(sms_notice)
        self.template_id = config.get("template_id", "")
        self.content = config.get("content", "")
        self.status = int(config.get("status", 0))
