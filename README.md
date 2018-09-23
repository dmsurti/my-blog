The markdown articles posted on my blog with all image assets.

I prefer to keep the content separate from the presentation. This separation
allows me to focus on writing and producing content instead of worrying about
how to present it.

I host my blog on [Weebly](http://www.deepaksurti.com/blog) rendered with the
[Lecia](https://boocare.weebly.com/leica.html) template. That takes care of
presenting it neatly.

With [Pandoc](https://pandoc.org), I can export the same content to multiple 
formats!

Blog Layout
---

I use Lecia's Blog Layout 3 which needs images to be placed at the top of the
blog post in the following dimensions: 660 * 660 px.

I draw these images in Paper app, export to my iMac, then use the online [Tuxpi
photo editor](https://www.tuxpi.com) to add border. Refer to
`utils/border-settings-wood.png` for the wooden frame border settings to apply.

Conventions
---

- Each blog post is placed in a directory rooted in a directory tree which is:
`yyyy/mm/dd`, which is the date of the post authoring.

- Blog post must be placed in a mardown file named `post.md`.

- The original source file from Paper app for the post header image is saved as
  `post-header.png`.

- The framed header file generated using Tuxpi is saved as `post.jpg` and is
  `660 * 660 px`.

- The post's pdf file can be generated using the `post.py` file:
  ```
  python utils/post.py -p 2011/12/14/value-of-tech-books
  
  Use the -v flag for verbose output of the post metadata
  ```

- The pdf files for all posts can also be generated with `post.py`:
  ```
  python utils/post.py -a

  Use the -v flag for verbose output of the post metadata
  ```

Python Utility
---

The python module `post.py` generates a post pdf content using `Pandoc`.

A [conda](https://conda.io/docs/user-guide/overview.html) environment defined
in `environment.yml` must be used to
[create](https://conda.io/docs/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)
an environment as per these requirements to execute/modify this python module.
