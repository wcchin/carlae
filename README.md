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
	
Then two directories: `docs` and `carlae_page` will be generated automatically:


    |- some_fancy_name
        |- fancy_src
        |- some_cool_stuff
            |- astonishing.png
            |- brilliant.png
            |- cool.png
        |- carlae_page
            |- theme
				|- css
				|- js
				|- _templates
					|- page.html
        |- docs
            |- css
            |- js
            |- index.html
        |- README.md

the carlae_page/theme/css and carlae_page/theme/js will be copied to docs when the `carlae` command is called (again).  
the carlae_page/theme/_templates/page.html is the jinja2 template file, which will be used to generate the docs/index.html, and this is the single static page for your readme file. 

## Add config file or front matter

Carlae rely on the front matter in the readme file to get the basic configuration. In latest version, **carlae will also try to find a file named carlae.conf for these configuration. **

Front matter should looks like:

	top_title: Carlae: A single static webpage generator
	project_name: Carlae
	smart_title: Super Simple Stupid Single Static webpage generator
	author: me
	short_description: simple short desc.
	keywords: [static, site, generator]
	three_concepts: [': typcn-device-desktop :', ': typcn-user-outline :', ': fas-keyboard :']
	three_desc: [the monitor, the user, and the keyboard]
	concept_color: '#33C3F0'
	project_url: https://github.com/wcchin/carlae
	project_url_title: Go to project page...
	carlae_dir: carlae_page

These are:

- top_title: The title that will be used in `<head><title> here </title></head>`
- project_name: the project name, which appear in the top of the page (body)
- smart_title: some smart and fancy words that make the project attractive 
- author: the name of the author who create this project
- short_description: in the description of meta 
- keywords: e.g. [static, site, generator], use square brackets to cover them, and comma to separate them
- three_concepts: use two colons to cover a simple terms, starting by fas to use fontawesome icons, or typcn to use typicons. The blank space should be remove in the above example. 
- three_desc: the three simple description about the three concept icons above
- concept_color: the color of the three concepts icons
- project_url: the project url
- project_url_title: words appear on the button link to the project url
- carlae_dir: OPTIONAL, the directory where Carlae will save and use the theme, you can modify it from here. it is default to `carlae_page`


Or, you can also tell carlae where the config file is through the -c optional argument, e.g.:

```
carlae -i README.md -c carlae_setting.conf
```


## on Github

Just a small reminder, after the docs/ directory to github, remember to turn the GitHub Pages setup on. 

The `Source` change to `master branch/docs folder` should be ok, and then the project page will appear at https://your_user_name.github.io/your_project_name .


# Some convenient stuff

## Using watch command

Carlae included watchdog package, which is used to watch the changes of the readme file, if it is changed (and saved), the carlae command will be trigger automatically, and generate the docs/index.html accordingly. 

run this if you want to use the watchdog feature:

	$ carlae -w 
	
## Using icons

Carlae added some function to detect the use of fontawesome and typicons. If you want to use these icons, write the name of the icon, and use two colons surrounding it, likes:

	:name_of_source-name_of_icons:
	
the available source are fontawesome (fas or fab) and typicons (typcn). for the name of icons, check the website: [fontawesome](https://fontawesome.com/) and [typicons](https://www.s-ings.com/typicons/)

For example (remove any space between the two colons): 

- : fas-keyboard : will becomes :fas-keyboard:
- : typcn-globe-outline : will becomes :typcn-globe-outline:


## Anchor point menu bar

The menu bar as shown in this page (skeleton theme) is also generated automatically during the conversion from markdown to html.  
It will convert the first (h1) and second (h2) level items into the menu, according to the sequence of appearance.

E.g.:

	# chapter I
	## section I-1
	## section I-2
	## section I-3
	# chapter II
	## section II-1
	## section II-2
	## section II-3
	# chapter III
	# chapter IV
	## section IV-1
	## section IV-2
	......
	
will convert to  

	chapter I | chapter II | chapter III | chapter IV......

each of the chapter I, II, and IV will have a dropdown menu showing the sections, and for chapter III, there will be a dropdown menu contain only chpater III itself. 


# Finishing

That's all for now. 

## Some example

- [pyreveal page](https://wcchin.github.io/pyreveal/index.html)
- [example of skeleton theme](https://wcchin.github.io/carlae/index.html)
- [example of minimal theme](https://wcchin.github.io/carlae/minimal/index.html)
- [example of poole theme](https://wcchin.github.io/carlae/poole/index.html)

## License 

MIT License

Copyright (c) 2019 Wei Chien Benny Chin <wcchin.88@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
