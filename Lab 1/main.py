import wget
import os, shutil, subprocess

from graph import Graph, EdgeType


DATASETS_PATH = './data'
DATASETS = [
    {
        'name': 'fb_graph',
        'url': 'https://snap.stanford.edu/data/facebook_combined.txt.gz',
        'edge_type': EdgeType.UNDIRECTED,
        'header_size': 0,
    },
    {
        'name': 'collaboration_network',
        'url': 'https://snap.stanford.edu/data/ca-GrQc.txt.gz',
        'edge_type': EdgeType.UNDIRECTED,
        'header_size': 4,
    }
]


def prepare_data():
    graphs = {}

    # Clean data directoroy
    shutil.rmtree(DATASETS_PATH)

    if not os.path.exists(DATASETS_PATH):
        os.makedirs(DATASETS_PATH)

    for ds in DATASETS:
        # Download dataset
        filename, extension = os.path.splitext(wget.download(ds['url'], DATASETS_PATH))

        # Extract archive
        assert extension == '.gz'
        subprocess.call(['gzip', '-d', filename])

        # Create graph
        graph = Graph.create_from_edge_list(file_path=filename,
                                            header_size=ds['header_size'],
                                            edge_type=ds['edge_type'])

        graphs[ds['name']] = graph

    return graphs


def main():
    graphs = prepare_data()
    print(graphs.keys())


if __name__ == '__main__':
    main()
