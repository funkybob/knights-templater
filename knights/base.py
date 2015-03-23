
import ast

from . import parse


class Template:
    def __init__(self, raw):
        self.raw = raw
        self.root = parse.parse(raw)

        code = ast.Expression(
            body=ast.ListComp(
                elt=ast.Call(
                    func=ast.Name(id='str', ctx=ast.Load()),
                    args=[
                        ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id='x', ctx=ast.Load()),
                                attr='render',
                                ctx=ast.Load()
                            ),
                            args=[
                                ast.Name(id='context', ctx=ast.Load()),
                            ], keywords=[], starargs=None, kwargs=None
                        ),
                    ], keywords=[], starargs=None, kwargs=None
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
        global_ctx = {
            'nodelist': self.root.nodelist,
            'context': dict(context),
        }

        return ''.join(eval(self.code, global_ctx, {}))
