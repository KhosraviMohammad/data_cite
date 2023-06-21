from builtins import quit
from itertools import count

from utils import Provider, Client, Doi, slice_list


def get_client_doi_count(*, consortium_id):
    client_and_doi = []
    client = Client(query_params={'consortium-id': consortium_id})
    client.get_all_data()
    cleared_data = client.get_main_data()
    all_clients = cleared_data.get('all_clients')
    for client_id in all_clients:
        doi = Doi(query_params={'client_id': client_id})
        doi.get_data(count=1)
        doi_count = doi.meta.get('total')
        client_and_doi.append({'client': client_id, 'doi_count': doi_count})
    return client_and_doi


if __name__ == '__main__':
    print(get_client_doi_count(consortium_id='daraco'))
