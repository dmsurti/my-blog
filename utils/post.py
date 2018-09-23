import argparse
import glob
import os
import sys
import tempfile
import yaml

"""
Run this module from the root of the repo directory as such:
    python utils/post.py -h

This is important as this covention is assumed to compute the directory path of
each blog post.

"""

def current_dir():
    """
    :return: The directory name of the current module.
    """
    return os.path.dirname(__file__)

def full_post_dir(post_dir):
    """
    :param post_dir: The relative path of the post directory rooted at the repo
    root directory.

    :return The absoulte full path of the post directory.
    """
    return os.path.abspath(os.path.join(current_dir(), '..', post_dir))

def hyperlink_header():
    """
    :return The hyperlink header as a string.
    """
    header_file = os.path.abspath(os.path.join(current_dir(),
                                              'link-header.txt'))
    with open(header_file, 'r') as hf:
        return hf.read()

def post_metadata(post_dir):
    """
    :param post_dir: The relative path of the post directory rooted at the repo
    root directory.

    :return: The post metadata header formatted in markdown.
    """
    post_md_file = os.path.abspath(os.path.join(full_post_dir(post_dir),
                                               'post.yaml'))
    post_md = yaml.load(open(post_md_file))
    title = '#' + ' ' + post_md['title']
    yyyy, mm, dd = post_date(post_dir)
    dt = '##' + ' ' + mm + '/' + dd + '/' + yyyy
    owner = '###' + ' ' + post_md['author'] + ', ' + post_md['website']
    tags = '####' + ' Categories: ' + post_md['categories']
    return title + '\n\n' + dt + '\n\n' + owner + '\n\n' + tags

def basedir_onelevel_up(dir_path):
    """
    :param dir_path: The directory path whose one level up is required.
    :return: The one level up of the directory path.
    """
    up = os.path.abspath(os.path.join(dir_path, '..'))
    return (up, os.path.basename(up))

def post_date(post_dir):
    """
    :param post_dir: The relative path of the post directory rooted at the repo
    root directory.
    :return: The post date as (year, month, date) tuple.
    """
    dd_dir, dd = basedir_onelevel_up(post_dir)
    mm_dir, mm = basedir_onelevel_up(dd_dir)
    yyyy_dir, yyyy = basedir_onelevel_up(mm_dir)
    return (yyyy, mm, dd)

def post_header_image(post_dir):
    """
    :param post_dir: The relative path of the post directory rooted at the repo
    root directory.
    :return The post header image formatted in markdown.
    """
    header_img_path =  os.path.abspath(os.path.join(full_post_dir(post_dir),
                                                    'post.jpg'))
    return '![]' + '(' + header_img_path + ')'

def post_content(post_dir):
    """
    :param post_dir: The relative path of the post directory rooted at the repo
    root directory.
    :return: The post content in markdown as a string.
    """
    post_file = os.path.abspath(os.path.join(full_post_dir(post_dir), 
                                             'post.md'))
    with open(post_file, 'r') as pf:
        return pf.read()

def full_post_content(post_dir):
    """
    :param post_dir: The relative path of the post directory rooted at the repo
    root directory.
    :return: The full post content with header, metadata formatted in markdown. 
    """
    return hyperlink_header() + '\n\n' +\
           post_metadata(post_dir) + '\n\n' +\
           post_header_image(post_dir) + '\n\n' +\
           post_content(post_dir)

def generate_pdf(post_dir, verbose=False):
    """
    Generates the post pdf in post directory.

    :param post_dir: The relative path of the post directory rooted at the repo
    root directory.
    :param verbose: The option to print post metadata during pdf generation.
    """
    print('-------- Generating Post PDF : ' + post_dir)
    if verbose:
        print_post_metadata(post_dir)
    d = full_post_dir(post_dir)
    post_pdf = os.path.abspath(os.path.join(full_post_dir(post_dir),
                                            'post.pdf'))
    print('Writing to pdf ' + post_pdf)
    temp_md = tempfile.NamedTemporaryFile(dir=d, suffix='.md')
    print(temp_md.name)
    with open(temp_md.name, 'w') as f:
        f.write(full_post_content(post_dir))
    with open(temp_md.name, 'r') as f:
        # Need to switch back to root directory after generating pdf
        from_dir = os.path.abspath(os.path.join(current_dir(), '..'))
        # Switch to post directory and generate pdf
        # This is required as we keep image names relative to post dir
        os.chdir(d)
        os.system('pandoc ' + f.name + ' -s -o ' + post_pdf)
        os.chdir(from_dir)

def content_dir():
    """
    :return: The root of the content directory.
    """
    return os.path.abspath(os.path.join(current_dir(), '..'))

def print_post_metadata(post_dir):
    """
    Print the post metadata. Useful for debugging and used when verbose option
    is set.

    :param post_dir: The relative path of the post directory rooted at the repo
    root directory.
    """
    print('-------- Post Metadata --------')
    print(current_dir())
    print(full_post_dir(post_dir))
    print(hyperlink_header())
    print(post_date(post_dir))
    print(post_metadata(post_dir))
    print(post_header_image(post_dir))
    print('-------- Post Content --------')
    print(full_post_content(post_dir))

def main():
    """
    The main interface to generate pdf posts.

    Provides command line options to generate pdf of a post given it's
    directory relative to root directory, or generate pdfs for all posts.

    Provides command line option to switch on verbose output that prints post
    metadata during pdf generation process.

    python utils/post.py -h will provide info for all options.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--post', type=str,
                        help='Generate pdf for post placed in directory')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Generate pdf for all content')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Display post metadata information')

    args = parser.parse_args()

    if args.post:
        post_dir = args.post
        generate_pdf(post_dir, args.verbose)
    elif args.all:
        post_dirs = [d[0] for d in os.walk(content_dir())
                    if len(glob.glob(os.path.join(d[0], 'post.md'))) > 0]
        for post_dir in post_dirs:
            generate_pdf(post_dir, args.verbose)

if __name__ == '__main__':
    main()
