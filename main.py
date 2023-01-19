from xml.etree import ElementTree
from pprint import pprint


def fetch_structure_data(data_path):
    nodes_ = []
    structure, demands = list(ElementTree.parse(data_path).getroot())
    nodes_tag, links_tag = list(structure)
    links_ = {}
    demands_ = {}

    # fetching info about nodes from xml file
    for node in nodes_tag:
        nodes_.append(node.get("id"))

    for link in links_tag:
        links_[link.get("id")] = (list(link)[0].text, list(link)[1].text, 0)

    for demand in demands:
        paths = []
        adm_paths = list(demand)[3]
        for ap in adm_paths:
            adm_path = []
            for p in ap:
                adm_path.append(p.text)
            paths.append(adm_path)
        demands_[demand.get("id")] = (list(demand)[0].text, list(demand)[1].text, list(demand)[2].text, paths)
    return (nodes_, links_, demands_)


if __name__ == '__main__':
    nodes_, links_, demands_ = fetch_structure_data("polska.xml")
    pprint(nodes_)
    pprint(links_)
    pprint(demands_)
    gene = {
        "demand_id": "Demand_0_10",
        'transponders' : [{'capacity' : 40,
                           'path': ['Link_0_10',
                                    'Link_1_10',
                                    'Link_1_7',
                                    'Link_7_9',
                                    'Link_2_9']
                           }]
    }

