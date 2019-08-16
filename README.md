---
top_title: Carlae, a simple stuipd single static webpage generator for project site
project_name: Carlae
smart_title: Simple Stupid Single-webpage generator
author: wcchin
short_description: a static single page for project site generator
template: page.html
keywords: [static, site, generator]
three_concepts: [':typcn-device-desktop:', ':typcn-user-outline:', ':typcn-keyboard:']
three_desc: [the monitor, the user, and the keyboard]
concept_color: '#33C3F0'
project_url: https://github.com/wcchin/carlae
project_url_title: go to project page
theme: skeleton
carlae_dir: carlae_page
---

# Carlae

**A Quick way to create simple stupid SINGLE STATIC WEBPAGE for your project.**

Carlae is an easy to use [Markdown][] driven single-page static site generator. It is designed with focuses putting on making simple and beautiful project page for your open source project. 
You can write the readme file as always, using markdown, and add a few yaml configuration info on top of the readme file, then run the simple build function, and the single page website is generated. 

You can also design and modify your own theme file from the theme file ship with this project, which is based on the skeleton css (website). Carlae uses jinja2 as the engine to generate html content, so the template file (page.html) is written integrated with jinja2. 

# Dependencies

Carlae is written in python 3.6. Carlae has a few dependencies:

- markdown
- pyyaml
- jinja2
- watchdog


# Getting Started

Clone or download the repository:  

	$ git clone https://github.com/wcchin/carlae.git

and put the files (extract them if download zip file) to `somewhere`, then 

	$ cd somewhere/
	$ pip install .

This will install the package at the current location and it is editable. 
This will also add carlae to your terminal function.

## Project example

A simple project folder can look like this, and there should have a README.md file in it:

    |- some_fancy_name
        |- fancy_src
        |- some_cool_stuff
            |- astonishing.png
            |- brilliant.png
            |- cool.png
        |- README.md


To use carlae, simple cd to that folder, and run `carlae`:

	$ cd some/path/to/the/some_fancy_name/
	$ carlae
	$ # OR 
	$ carlae -i README.md
	



**write till here**

Create and build a site project:

    $ mkdir /path/to/site/project
    $ cd /path/to/site/project
    $ poole.py --init --theme minimal
    $ poole.py --build
    $ poole.py --serve

Done. You've just created a website! Browse <http://localhost:8080/> and watch
the example pages which have been created during initialization. To write your
own pages, use the example pages in the *input* folder as a starting point.

Next to the *miniaml* theme, there are some other [choices available][themes].

Run `poole.py --build` whenever you've made some changes in the *input* folder.

[zip]: http://bitbucket.org/obensonne/poole/get/default.zip
[tgz]: http://bitbucket.org/obensonne/poole/get/default.tar.gz
[zip3]: https://bitbucket.org/obensonne/poole/get/py3.zip
[tgz3]: http://bitbucket.org/obensonne/poole/get/py3.tar.gz
[themes]: https://bitbucket.org/obensonne/poole/wiki/Themes

# How It Works

Poole takes files from a project's `input` directory and copies them to the
`output` directory. In this process files ending with *md*, *mkd*, *mdown* or
*markdown* get converted to HTML using the project's `page.html` as a template
(unless a custom template is set on an individual page).

Additionally Poole expands any macros used in a page. Don't care about that for
now ..

When running `poole.py --build` in a Poole project, an input directory like
this:

    |- input
        |- index.md
        |- news.mkd
        |- foo.mdown
        |- images
            |- bar.png

will result in an output folder like that:

    |- output
        |- index.html
        |- news.html
        |- foo.html
        |- images
            |- bar.png

# Page Layout

Every Poole page is based on the skeleton file `page.html`. Hence adjusting the
site layout means adjusting `page.html` and extending or replacing its CSS file
`input/poole.css`.

The only thing you should keep in `page.html` are the embedded
{{\_\_content\_\_}} and {{\_\_encoding\_\_}} expressions.  Below is an almost
minimal `page.html` file. It does not look nice but it's a clean starting point
to build your own layout from scratch.

Minimal `page.html`:

    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset={{ __encoding__ }}" />
      </head>
      <body>
        {{ __content__ }}
      </body>
    </html>

It's easy to apply one of the numerous free CSS templates out there to a Poole
site. For more information read [this blog post with step-by-step
instructions][pimp].

In case you need special templates for individual pages, you can add the
property `tempalte` in the front matter of each page:

    title: This looks different
    template: a-special-page-template.html
    ---

In that case the given file is used as the page template instead of the default
`page.html` file.

[pimp]: http://obensonne.bitbucket.org/blog/20091122-using-a-free-css-templates-in-poole.html

## Content Generation

Poole allows you to embed Python code in your pages to *generate* content:

`input/some-page.md`:

    Here is normal text in *markdown* flavor.
    {%
    print "hello poole"
    %}
    Did you know? The sum of 2 and 2 is {{ 2 + 2 }}.

This example demonstrates two ways to embed Python code, either as statements or
as expressions:

  1. Everything between `{%` and `%}` are *statements* and whatever is printed
     to *stdout* during their execution is going to be part of the final HTML
     page.
  2. Everything between `{{` and `}}` are *expressions* and their evaluation is
     going to be part of the final page.

**TIP**: Instead of the outer curly brackets `{` and `}` you can also use
`<!--` and `-->` to prevent syntax highlighting markdown editors from getting
confused by the Python code.

**TIP:** To print the code surrounding tags literally, simply escape the
opening tag with a backslash.

[hyde]: http://ringce.com/hyde

### Outsource complex or frequently used code

To keep embedded code short and compact or to reuse it in several pages, it can
be outsourced into a file called `macros.py` in a project's root folder (where
the `page.html` file is located). Every public attribute in `macros.py` is
available within embedded Python code blocks:

`macros.py`:

    from datetime import date
    def today():
        return date.today().strftime("%B %d, %Y")

    author = "Popeye"

`input/some-page.md`:

    This site has been updated on {{ today() }} by {{ author }}.

### Builtin macros

Builtin macros can be used from the macros module as well as from python
code in your pages and templates (just as if they are defined within
your macros.py).

Currently, there is only one builtin macro available.

`hx(s)`

> Replace the characters that are special within HTML (`&`, `<`, `>` and `"`)
> with their equivalent character entity (e.g., `&amp;`). This should be
> called whenever an arbitrary string is inserted into HTML (i.e. use
> `{{ hx(variable) }}` instead of `{{ variable }}`). You do not need this
> within a markdown context.
>
> Note that `"` is not special in most HTML, only within attributes.
> However, since escaping it does not hurt within normal HTML, it is
> just escaped unconditionally.

### Working with pages

Next to stuff defined in `macros.py` the objects `page` and `pages` are
available in embedded Python code. The first one is a dictionary describing the
page in which the code is embedded. The second one is a list of *all* pages in
the project.

The following attributes are always set in a page dictionary:

  * **title:** The page's title, by default its filename without extension
    (setting alternatives is described in the next section).
  * **fname:** Path to the page's source file, e.g.
    `/path/to/project/input/stuff/news.md`.
  * **url:** The page's relative URL, e.g. for a source page
    `input/stuff/news.md` this is `stuff/news.html`.

The example `page.html` file in a freshly initialized site project uses a
page's *title* attribute:

    ...
    <div id="header">
         <h1>a poole site</h1>
         <h2>{{ page["title"] }}</h2>
    </div>
    ...

**TIP:** All items in a page dictionary are exposed as attributes, i.e.
`page["foobar"]` is identical to `page.foobar`. Dictionary access is useful if
an item may not be set, e.g.: `page.get("foobar", "...")`.

### Setting page attributes

Page attributes can be set at the top of a page's source file, in [Python's
configuration file style][pyconf]. They are delimited from the page's content
by a line with 3 or more dashes.

`input/stuff/news.md`:

    title: Hot News
    foobar: King Kong
    ---
    Here are some news about {{ page.foobar }}.
    Did I say {% print(page.foobar) %}?

That way you can also set a page's title explicitly, instead of using the file
name. Other useful attributes to set are *description* and *keywords*, which
get used by the default `page.html` file to set HTML meta tags. Here it comes
in handy to set *default* page attributes in the `macros.py` file:

`macros.py`:

    page = { "description": "some stuff", "keywords": "stuff" }

That way you can safely use the *description* and *keywords* attributes without
bothering if they are really defined in every page.

[pyconf]: http://docs.python.org/library/configparser.html

### Accessing page objects in the macros module

The objects `pages` and `page` are also available within `macros.py`. That
means you can define them as dummys and reference them in `macros.py`. Poole
updates them when loading the `macros` module.

`macros.py`:

    page = {} # you can also set defaults here, see previous section
    pages = []

    def something():
        # when executing this, the page and pages objects above are up-to-date
        print page["title"]

## Options and paths

Similarly to `page` and `pages` the following objects are available within
embedded Python code and within the *macros* module:

  * **options:** The command line arguments given to Poole as parsed by
    [Python's optparse module][pyopts]. For instance the base URL can be
    retrieved by `options.base_url`.
  * **project:** Path to the project's root directory.
  * **input:** Path to the project's input directory.
  * **output:** Path to the project's output directory.

[pyopts]: http://docs.python.org/library/optparse.html

### Character encodings

In case you use non-ASCII characters, check the *encoding* options of Poole. In
most cases working with non-ASCII strings should work straight forward if the
options are set properly (default is *UTF-8*).

However, be aware that page variables defined within page source files and
derived from a page's file name internally are handled as Python *unicode*
objects. That means if you want to refer to non-ASCII page variable names and
values form within embedded Python code or from `macros.py`, make sure to use
*unicode* strings to reference them.

### Custom file converters

If you use [LESS][] or [CleverCSS][] you'll be happy about the possibility to
define custom converters Poole applies to selected files in its building
process. Custom converters may be defined in `macros.py` using a dictionary
named 'converter' with file name patterns as keys and a converter function as
well as a target file name extension as values:

    converter = {
        r'\.ccss': (ccss_to_css, 'css'),
        ...
    }

The converter function `ccss_to_css` must accept the source file name and the
destination file name as arguments. The destination file name is a suggestion
(the source filename mapped to the project's output directory with the
extension given in the converter dictionary) - you are free to choose another
one:

    import clevercss

    def ccss_to_css(src, dst):
        # when `src` is '/path/to/project/input/foo.ccss'
        # then `dst` is '/path/to/project/output/foo.css'
        ccss = open(src).read()
        css = clevercss.convert(ccss)
        open(dst, 'w').write(css)

[clevercss]: http://sandbox.pocoo.org/clevercss/
[less]: http://lesscss.org/

### Pre- and post-convert hooks

All pages converted by Poole may be processed by custom code in `macros.py`
using *hook* functions. In particular, any function whose name starts with
`hook_preconvert_` is run after source markdown files have been parsed but
not yet converted. Similarly, any function whose name starts with
`hook_postconvert_` is run after the content of pages has been converted to
HTML (but still without the skeleton HTML given in the project's `page.html`
file).

Pre-convert hooks are useful to preprocess the markdown source and/or to
generate new virtual pages based on existing real pages:

    def hook_preconvert_foo():
        # important: replace all foos by bars in every page
        for p in pages:
            p.source = p.source.replace("foo", "bar")
        # create a new virtual page which still has a foo
        p = Page("foo.md", virtual="The only page with a *foo*.", title="Foony")
        pages.append(p)

Virtual pages can be created by providing a virtual source filename relative
to the project's input folder and corresponding markdown content. Page
attributes (e.g. `title`) may be given as additional keyword arguments but
may also be encoded in the markdown source as in real markdown input files.

A common use case for post-convert hooks is to generate full content RSS feeds:

    def hook_postconvert_rss():
        # this is kind of pseudo code
        rss = ...
        for p in pages:
            rss.add_item(..., r.html)
        rss.save(".../rss.xml")

More practical and detailed usage examples of hooks and virtual pages can be
found in the recipes.

### Recipes

You can do some pretty fancy and useful things with inlined Python code and
the macros module, for instance generate a list of blog posts or create an RSS
file. Check out the [example recipes][recipes].

[recipes]: https://bitbucket.org/obensonne/poole/wiki/Recipes

## Feedback

Please use the [issue tracker][issues].

[issues]: http://bitbucket.org/obensonne/poole/issues/
