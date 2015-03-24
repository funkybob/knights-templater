
import ast

from . import parse


class Template:
    def __init__(self, raw):
        self.raw = raw
        self.parser = parse.Parser(raw)
        self.nodelist = self.parser()

        code = ast.Expression(
            body=ast.GeneratorExp(
                elt=ast.Call(
                    func=ast.Name(id='str', ctx=ast.Load()),
                    args=[
                        ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id='x', ctx=ast.Load()),
                                attr='render',
                                ctx=ast.Load()
                            ),
                            args=[ast.Name(id='context', ctx=ast.Load())],
                            keywords=[], starargs=None, kwargs=None
                        ),
                    ],
                    keywords=[], starargs=None, kwargs=None
                ),
                generators=[
                    ast.comprehension(
                        target=ast.Name(id='x', ctx=ast.Store()),
                        iter=ast.Name(id='nodelist', ctx=ast.Load()),
                        ifs=[]
                    ),
                ]
            )
        )

        ast.fix_missing_locations(code)
        self.code = compile(code, filename='<template>', mode='eval')

    def render(self, context):
        ctx = dict(context, _filter=self.parser.filters, _tag=self.parser.tags)
        global_ctx = {
            'nodelist': self.nodelist,
            'context': ctx,
        }

        return ''.join(eval(self.code, global_ctx, {}))
