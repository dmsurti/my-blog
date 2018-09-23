import os
import sys
import tempfile
import yaml

def current_dir():
    return os.path.dirname(__file__)

def full_post_dir(post_dir):
    return os.path.abspath(os.path.join(current_dir(), '..', post_dir))

def hyperlink_header():
    header_file = os.path.abspath(os.path.join(current_dir(),
                                              'link-header.txt'))
    with open(header_file, 'r') as hf:
        return hf.read()

def post_metadata(post_dir):
    post_md_file = os.path.abspath(os.path.join(full_post_dir(post_dir),
                                               'post.yaml'))
    post_md = yaml.load(open(post_md_file))
    title = '#' + ' ' + post_md['title']
    yyyy, mm, dd = post_date(post_dir)
    dt = '##' + ' ' + mm + '/' + dd + '/' + yyyy
    owner = '###' + ' ' + post_md['author'] + ', ' + post_md['website']
    return title + '\n\n' + dt + '\n\n' + owner

def basedir_onelevel_up(dir_path):
    up = os.path.abspath(os.path.join(dir_path, '..'))
    return (up, os.path.basename(up))

def post_date(post_dir):
    dd_dir, dd = basedir_onelevel_up(post_dir)
    mm_dir, mm = basedir_onelevel_up(dd_dir)
    yyyy_dir, yyyy = basedir_onelevel_up(mm_dir)
    return (yyyy, mm, dd)

def post_header_image(post_dir):
    header_img_path =  os.path.abspath(os.path.join(full_post_dir(post_dir),
                                                    'post.jpg'))
    return '![]' + '(' + header_img_path + ')'

def post_content(post_dir):
    post_file = os.path.abspath(os.path.join(full_post_dir(post_dir), 
                                             'post.md'))
    with open(post_file, 'r') as pf:
        return pf.read()

def full_post_content(post_dir):
    return hyperlink_header() + '\n\n' +\
           post_metadata(post_dir) + '\n\n' +\
           post_header_image(post_dir) + '\n\n' +\
           post_content(post_dir)

def generate_pdf(post_dir):
    d = full_post_dir(post_dir)
    post_pdf = os.path.abspath(os.path.join(full_post_dir(post_dir),
                                            'post.pdf'))
    print('Writing to pdf ' + post_pdf)
    temp_md = tempfile.NamedTemporaryFile(dir=d, suffix='.md')
    print(temp_md.name)
    with open(temp_md.name, 'w') as f:
        f.write(full_post_content(post_dir))
    with open(temp_md.name, 'r') as f:
        os.chdir(d)
        os.system('pandoc ' + f.name + ' -s -o ' + post_pdf)

if __name__ == '__main__':
    post_dir = sys.argv[1]
    print('-------- Post Metadata --------')
    print(post_dir)
    print(current_dir())
    print(full_post_dir(post_dir))
    print(hyperlink_header())
    print(post_date(post_dir))
    print(post_metadata(post_dir))
    print(post_header_image(post_dir))
    print('-------- Post Content --------')
    print(full_post_content(post_dir))
    print('-------- Generating Post PDF --------')
    generate_pdf(post_dir)
