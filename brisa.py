#!/usr/bin/env python3
"""Interpretador da Brisa, uma linguagem pequena executada a partir de arquivos.

Não existe modo interativo: passe sempre o caminho de um arquivo .brisa.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class BrisaError(Exception):
    """Erro apresentado ao autor de um programa Brisa."""


@dataclass
class Line:
    number: int
    indent: int
    text: str


def read_lines(source: str) -> list[Line]:
    lines: list[Line] = []
    for number, raw in enumerate(source.splitlines(), start=1):
        text = raw.split("#", 1)[0].rstrip()
        if not text:
            continue
        indent = len(text) - len(text.lstrip(" "))
        if indent % 2:
            raise BrisaError(f"linha {number}: use grupos de dois espaços para indentar")
        lines.append(Line(number, indent, text.lstrip()))
    return lines


def value(expression: str, names: dict[str, Any], line: int) -> Any:
    """Avalia somente expressões simples e seguras da Brisa."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as error:
        raise BrisaError(f"linha {line}: expressão inválida: {expression}") from error

    allowed = (
        ast.Expression, ast.Constant, ast.Name, ast.Load, ast.BinOp, ast.UnaryOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.USub, ast.UAdd,
        ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.BoolOp, ast.And, ast.Or, ast.Not,
    )
    for node in ast.walk(tree):
        if not isinstance(node, allowed):
            raise BrisaError(f"linha {line}: esta expressão não é permitida")
    try:
        return eval(compile(tree, "<brisa>", "eval"), {"__builtins__": {}}, names)
    except NameError as error:
        raise BrisaError(f"linha {line}: nome desconhecido") from error
    except (ArithmeticError, TypeError) as error:
        raise BrisaError(f"linha {line}: não foi possível calcular a expressão") from error


def run_block(lines: list[Line], start: int, indent: int, names: dict[str, Any]) -> int:
    index = start
    while index < len(lines):
        current = lines[index]
        if current.indent < indent:
            return index
        if current.indent > indent:
            raise BrisaError(f"linha {current.number}: indentação inesperada")

        if current.text.startswith("crie "):
            try:
                name, expression = current.text[5:].split(" = ", 1)
            except ValueError as error:
                raise BrisaError(f"linha {current.number}: escreva `crie nome = valor`") from error
            if not name.isidentifier():
                raise BrisaError(f"linha {current.number}: `{name}` não é um nome válido")
            names[name] = value(expression, names, current.number)
            index += 1
        elif current.text.startswith("diga "):
            print(value(current.text[5:], names, current.number))
            index += 1
        elif current.text.startswith("repita ") and current.text.endswith(":"):
            times = value(current.text[7:-1], names, current.number)
            if not isinstance(times, int) or isinstance(times, bool) or times < 0:
                raise BrisaError(f"linha {current.number}: `repita` precisa de um número inteiro positivo")
            child = index + 1
            if child == len(lines) or lines[child].indent <= indent:
                raise BrisaError(f"linha {current.number}: falta o bloco de `repita`")
            end = block_end(lines, child, indent)
            for _ in range(times):
                run_block(lines[child:end], 0, lines[child].indent, names)
            index = end
        elif current.text.startswith("se ") and current.text.endswith(":"):
            child = index + 1
            if child == len(lines) or lines[child].indent <= indent:
                raise BrisaError(f"linha {current.number}: falta o bloco de `se`")
            end = block_end(lines, child, indent)
            if value(current.text[3:-1], names, current.number):
                run_block(lines[child:end], 0, lines[child].indent, names)
            index = end
        else:
            raise BrisaError(f"linha {current.number}: não entendi `{current.text}`")
    return index


def block_end(lines: list[Line], start: int, parent_indent: int) -> int:
    index = start
    while index < len(lines) and lines[index].indent > parent_indent:
        index += 1
    return index


def run(source: str) -> None:
    lines = read_lines(source)
    run_block(lines, 0, 0, {})


def main(arguments: list[str]) -> int:
    if len(arguments) != 2:
        print("Uso: python3 brisa.py caminho/do/programa.brisa", file=sys.stderr)
        return 2
    path = Path(arguments[1])
    try:
        run(path.read_text(encoding="utf-8"))
    except (OSError, BrisaError) as error:
        print(f"Brisa: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
