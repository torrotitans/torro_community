import abc
import re
class stageBase(metaclass=abc.ABCMeta):

    base_para = {"id": {"type": int, "default": -1},
                 "label": {"type": str, "default": ''},
                 "flowType": {"type": str, "default": ''},
                 "apiTaskName": {"type": str, "default": ''},
                 "condition": {"type": list(), "default": []}}
    sql_ignore_set = set(["\"", "\\", "/", "*", "'", "=", "-", "#", ";",
                          "<", ">", "+", "%", "$", "(", ")", "%", "!",
                          'drop table', 'delete from', 'select *'])
    pattern = '\$\(.*?\)'

    @staticmethod
    def save_pattern(text):
        mapping_words = re.findall(stageBase.pattern, text)
        for mapping_word in mapping_words:
            save_word = mapping_word.replace('$(', '&|_|').replace(')', '_|')
            text = text.replace(mapping_word, save_word)
        return text, mapping_words
    @staticmethod
    def recover_pattern(text, mapping_words):
        for mapping_word in mapping_words:
            save_word = mapping_word.replace('$(', '&|_|').replace(')', '_|')
            text = text.replace(save_word, mapping_word)
        return text
    @staticmethod
    def verify_all_param(verify_all_param, stage_dict):
        new_stage_dict = verify_all_param(stage_dict, stageBase.base_para)
        # # print('stage: ', stage_dict)
        if new_stage_dict['flowType'] == 'Trigger':
            return new_stage_dict
        else:
            for index, condition in enumerate(new_stage_dict['condition']):
                # print('check condition', new_stage_dict)
                if str(condition['style']) != '3' and  str(condition['style']) != '5':
                    text = new_stage_dict['condition'][index]['value']
                    text, mapping_words = stageBase.save_pattern(text)
                    for ignore_word in stageBase.sql_ignore_set:
                        text = text.replace(ignore_word, '')
                    text = stageBase.recover_pattern(text, mapping_words)
                    new_stage_dict['condition'][index]['value'] = text
            return new_stage_dict