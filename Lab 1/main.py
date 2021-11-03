import wget
import pathlib
import os, shutil, subprocess


def prepare_data(use_cached=False):
    DOWNLOAD_PATH = './data'

    if not use_cached:
        shutil.rmtree(DOWNLOAD_PATH)
    elif os.path.exists(DOWNLOAD_PATH):
        return

    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    urls = [
        'https://snap.stanford.edu/data/facebook.tar.gz',
        'https://snap.stanford.edu/data/facebook_combined.txt.gz',
        'https://snap.stanford.edu/data/ca-GrQc.txt.gz'
    ]

    # Download datasets
    filenames = []
    for url in urls:
        filename = wget.download(url, DOWNLOAD_PATH)
        filenames.append(filename)

    # Extract archives
    for filename in filenames:
        extension = ''.join(pathlib.Path(filename).suffixes)
        if extension == '.tar.gz':
            subprocess.call(['tar', '-xf', filename, '-C', DOWNLOAD_PATH])
        else:  # .gz
            subprocess.call(['gzip', '-d', filename])


def main():
    prepare_data(use_cached=True)


if __name__ == '__main__':
    main()
