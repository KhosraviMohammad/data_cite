from builtins import quit
from itertools import count

from utils import Provider, Client, Doi, slice_list


def get_client_doi_count(*, consortium_id):
    client_and_doi = []
    provide = Provider(query_params={'consortium-id': consortium_id})
    provide.get_all_data()
    provide_client_list = provide.get_clients()
    for client_id in provide_client_list:
        doi = Doi(query_params={'client_id': client_id})
        doi.get_data(count=1)
        doi_count = doi.meta.get('total')
        client_and_doi.append({'client': client_id, 'doi_count': doi_count})
    return client_and_doi


def get_client_doi_count_method2(*, consortium_id):
    client_and_doi = []
    provide = Provider(query_params={'consortium-id': consortium_id})
    provide.get_all_data()
    doi = Doi(query_params={'consortium-id': consortium_id})
    doi.get_all_data()
    doi_main_information = doi.get_main_data()
    provide_client_list = provide.get_clients()
    for client_id in provide_client_list:
        if client_id not in doi_main_information:
            doi_main_information.update({client_id: {'doi_ids': [], 'count': 0}})

    for client_id, information in doi_main_information.items():
        doi_count = information.get('count')
        client_and_doi.append({'client': client_id, 'doi_count': doi_count})

    return client_and_doi


if __name__ == '__main__':
    print(get_client_doi_count(consortium_id='daraco'))
