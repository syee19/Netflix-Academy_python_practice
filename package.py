# -*- coding: utf-8 -*-

name = 'sinyulee'
version = '1.0.5'
authors = ['Sinyu Lee']
requires = [
    'python',
]
variants = [
    ['platform-linux', 'python'],
]
tools = ['todo']

def commands():
    env.PATH.append("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")


format_version = 2
