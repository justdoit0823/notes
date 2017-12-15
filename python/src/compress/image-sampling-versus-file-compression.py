
"""Compare sampling image with compressing file."""

import gzip
import os
import sys

from PIL import Image


def show_sampling_and_compression(path):
    """Show reducing size of sampling and compression."""
    origin_size = os.stat(path).st_size

    filename, ext = os.path.splitext(path)

    img_obj = Image.open(path)
    f_format = img_obj.format

    # sampling files
    sample_rates = (90, 80, 70, 60, 50, 40)
    sample_paths = []
    sample_sizes = []
    for rate in sample_rates:
        sample_path = filename + str(rate) + ext
        img_obj.save(sample_path, f_format, quality=rate)
        sample_paths.append(sample_path)

    # show size of the samples
    print('original size %d bytes.' % origin_size)
    for idx, sample_path in enumerate(sample_paths):
        sample_size = os.stat(sample_path).st_size
        sample_sizes.append(sample_size)
        print('%f quality size %d bytes, percent %.2f%%.' % (
            sample_rates[idx], sample_size, 100 *(sample_size / origin_size)))

    print()

    # calculate compression rate of the origin
    with open(path, 'rb') as f:
        data = f.read()

    for level in range(10):
        origin_zip_size = len(gzip.compress(data, level))
        print('original file at compression level %d, and size %d, '
              'percent %.2f%%.' % (
                  level, origin_zip_size,
                  100 * (origin_zip_size / origin_size)))

    print()

    # calculate compression rate of the samples
    for idx, sample_path in enumerate(sample_paths):
        with open(sample_path, 'rb') as f:
            data = f.read()
            for level in range(10):
                sample_zip_size = len(gzip.compress(data, level))
                print('%f sample file at compression level %d, and size %d, '
                      'percent %.2f%%.' % (
                          sample_rates[idx], level, sample_zip_size,
                          100 * (sample_zip_size / sample_sizes[idx])))

        print()

    # cleanup temporary files
    img_obj.close()
    for sample_path in sample_paths:
        os.remove(sample_path)


def main():
    if len(sys.argv) < 2:
        print('empty image file.')
        return

    path = sys.argv[1]
    show_sampling_and_compression(path)


if __name__ == '__main__':

    main()
