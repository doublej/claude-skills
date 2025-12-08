#!/usr/bin/env python3
"""Generate ERD diagrams from Python data model classes."""
import argparse
import importlib
import sys
from pathlib import Path


def import_model(dotted_path: str):
    """Import a model class from dotted path like 'mymodule.submodule.MyModel'."""
    module_path, _, class_name = dotted_path.rpartition(".")
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def generate_erd(
    model_path: str,
    output: str,
    graph_attr: dict | None = None,
    node_attr: dict | None = None,
    edge_attr: dict | None = None,
):
    """Generate ERD diagram for a model class."""
    import erdantic as erd

    model = import_model(model_path)
    diagram = erd.create(model)
    diagram.draw(
        output,
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
    )
    return diagram


def main():
    parser = argparse.ArgumentParser(description="Generate ERD from Python models")
    parser.add_argument("model", help="Dotted path to model class (e.g., myapp.models.User)")
    parser.add_argument("-o", "--output", default="diagram.png", help="Output file path")
    parser.add_argument("--nodesep", type=float, help="Vertical spacing between nodes")
    parser.add_argument("--ranksep", type=float, help="Horizontal spacing between ranks")
    parser.add_argument("--fontsize", type=int, help="Font size for labels")
    args = parser.parse_args()

    graph_attr = {}
    if args.nodesep:
        graph_attr["nodesep"] = str(args.nodesep)
    if args.ranksep:
        graph_attr["ranksep"] = str(args.ranksep)
    if args.fontsize:
        graph_attr["fontsize"] = str(args.fontsize)

    diagram = generate_erd(
        args.model,
        args.output,
        graph_attr=graph_attr or None,
    )
    print(f"Generated ERD: {args.output}")
    print(f"Models: {list(diagram.models.keys())}")


if __name__ == "__main__":
    main()
