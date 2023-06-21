from logging.config import valid_ident

import requests
import json


class DataCite:
    base_url = "https://api.test.datacite.org/{end_point}?{query_params}"
    headers = {"accept": "application/vnd.api+json"}

    def __init__(self, end_point, query_params=None, headers=None):
        self.end_point = end_point
        self.query_params = DataCite.parse_query_params(query_params=query_params)
        self.headers = headers or self.headers
        self.base_url = self.base_url.format(end_point=self.end_point, query_params=self.query_params)

    @classmethod
    def parse_query_params(cls, query_params=None):
        query_params = query_params or {}
        parsed_query_prams = ''
        for param_name, value in query_params.items():
            parsed_query_prams += param_name + '=' + str(value) + '&'
        return parsed_query_prams

    def get_data(self, page=1, count=100):
        url = self.base_url + f"page[size]={count}&page[number]={page}"
        response = requests.get(url, headers=self.headers)
        response_content = json.loads(response.content)
        data = response_content.get('data')
        meta = response_content.get('meta')
        self.item_count = meta.get('total')
        self.current_page = meta.get('page')
        self.page_count = meta.get('totalPages')
        self.meta = meta
        setattr(self, self.__class__.__name__.lower() + 's', data)

    def get_all_data(self, *args, **kwargs):
        base_url = self.base_url + "page[size]=1000&{page}"
        url = base_url.format(page='')
        response = requests.get(url, headers=self.headers)
        response_content = json.loads(response.content)
        data = response_content.get('data')
        meta = response_content.get('meta')
        item_count = meta.get('total')
        current_page = meta.get('page')
        page_count = meta.get('totalPages')
        for page in range(current_page + 1, page_count + 1):
            url = base_url.format(page=f'page[number]={page}')
            response = requests.get(url, headers=self.headers)
            response_content = json.loads(response.content)
            next_page_data = response_content.get('data')
            data.extend(next_page_data)
        self.meta = meta
        setattr(self, self.__class__.__name__.lower() + 's', data)

    @classmethod
    def make_query_value(self, values):
        query_value = f'({values[0]}/*)'
        for value in values[1:len(values) - 1]:
            query_value += f'OR({value}/*)'
        return query_value

    def cache(self, *args, **kwargs):
        pass

    def get_cache(self, *args, **kwargs):
        pass


class Doi(DataCite):
    end_point = "dois"

    def __init__(self, query_params=None):
        super(Doi, self).__init__(end_point=self.end_point, query_params=query_params)


class Client(DataCite):
    end_point = "clients"

    def __init__(self, query_params=None):
        super(Client, self).__init__(end_point=self.end_point, query_params=query_params)

    def get_main_data(self):
        clients = self.clients
        cleared_client_data_list = []
        all_prefixes = []
        all_clients = []
        for client in clients:
            id = client.get('id')
            relationships = client.get('relationships')
            prefixes = relationships.get('prefixes').get('data')
            cleared_prefixes = []
            for index in range(len(prefixes)):
                cleared_prefixes.append(prefixes[index].get('id'))
                all_prefixes.append(prefixes[index].get('id'))
            cleared_client_data = {
                'id': id,
                'prefixes': cleared_prefixes,
            }
            all_clients.append(id)
            cleared_client_data_list.append(cleared_client_data)
        return {'main_data': cleared_client_data_list, 'all_prefixes': all_prefixes, 'all_clients': all_clients}


class Provider(DataCite):
    end_point = "providers"

    def __init__(self, query_params=None):
        super(Provider, self).__init__(end_point=self.end_point, query_params=query_params)


def slice_list(num, list_to_break):
    broken_list = []
    for index, item in enumerate(list_to_break):
        index += 1
        broken_list.append(item)
        print(index % num)
        if index % num == 0:
            yield broken_list
            broken_list = []
    else:
        if len(broken_list) != 0:
            yield broken_list
