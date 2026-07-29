from __future__ import annotations

import ast
import operator
from typing import Any

from tools._shared import err

_OP_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg
}

def _eval(node: Any) -> Any:
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        return _OP_MAP[type(node.op)](_eval(node.left), _eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        return _OP_MAP[type(node.op)](_eval(node.operand))
    else:
        raise TypeError("Unsupported node type")

def calculate(expression: str = "") -> dict[str, Any]:
    """Evaluates a mathematical expression safely."""
    try:
        if not expression:
            raise ValueError("Expression cannot be empty.")
        # replace ^ with ** for python eval
        expr = expression.replace('^', '**')
        node = ast.parse(expr, mode='eval').body
        result = _eval(node)
        return {
            "tool": "calculator",
            "expression": expression,
            "result": result
        }
    except Exception as exc:
        return err("calculator", exc)
