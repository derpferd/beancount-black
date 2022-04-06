# beancount-black
Opinionated code formatter, just like Python's [black](https://pypi.org/project/black/) code formatter but for Beancount

# Sponsor

This project is sponsored by [BeanHub](https://beanhub.io) -- a modern accounting book service based on the most popular open source version control system [Git](https://git-scm.com/) and text-based double entry accounting book software [Beancount](https://beancount.github.io/docs/index.html).

## Install

To install the formatter, simply run

```bash
pip install beancount-black
```

## Usage

Run

```bash
bean-black /path/to/the/file.bean
```

Then the file will be formatted.
Since this tool is still in its early stage, a backup file at `<filepath>.backup` will be created automatically by default.
The creation of backup files can be disabled by passing `-n` or `--no-backup` like this

```bash
bean-black /path/to/the/file.bean
```

It's highly recommended to use [BeanHub](https://beanhub.io), Git or other version control system to track your Beancount book files before running the formatter against them without a backup.
