"""Mirrors sqlalchemy/test/orm/inheritance/test_poly_linked_list.py :: PolymorphicCircularTest

Node + NodeB + Node2/Node3 form a
self-referential linked list.  related_id on Node points to the previous
node; the nxt relationship resolves to the node whose related_id equals
the current node's id.
"""

from typing import Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


def _make_classes():
    class Node(SQLModel, table=True):
        __tablename__ = "ll_node"
        id: Optional[int] = Field(default=None, primary_key=True)
        type: str = Field(default="node")
        name: str
        # FK points to the *previous* node (my predecessor's id)
        related_id: Optional[int] = Field(default=None, foreign_key="ll_node.id")

        # nxt: the node whose related_id == my id (i.e. the successor)
        nxt: Optional["Node"] = Relationship(
            sa_relationship_kwargs={
                "primaryjoin": "Node.id == Node.related_id",
                "foreign_keys": "[Node.related_id]",
                "uselist": False,
            }
        )

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "node",
        }

    class NodeB(Node):
        __mapper_args__ = {"polymorphic_identity": "nodeb"}

    class Node2(Node, table=True):
        __tablename__ = "ll_node2"
        id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="ll_node.id"
        )
        __mapper_args__ = {"polymorphic_identity": "node2"}

    class Node3(Node, table=True):
        __tablename__ = "ll_node3"
        id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="ll_node.id"
        )
        __mapper_args__ = {"polymorphic_identity": "node3"}

    return Node, NodeB, Node2, Node3


def _build_chain(db, *nodes):
    """Persist nodes and wire nxt: nodes[0] → nodes[1] → … → nodes[-1]."""
    db.add_all(nodes)
    db.flush()
    for i in range(len(nodes) - 1):
        nodes[i].nxt = nodes[i + 1]
    db.commit()
    return nodes[0].id, nodes[-1].id


def _traverse_forward(db, Node, head_id):
    node = db.get(Node, head_id)
    names, types = [], []
    while node:
        names.append(node.name)
        types.append(type(node).__name__)
        node = node.nxt
    return names, types


def _traverse_backward(db, Node, tail_id):
    node = db.get(Node, tail_id)
    names = []
    while node:
        names.append(node.name)
        if node.related_id is None:
            break
        node = db.get(Node, node.related_id)
    return names


def test_linked_list_jti_chain():
    """ nodes chain: Node → Node2 → Node → Node2 (mirrors test_one)."""
    Node, NodeB, Node2, Node3 = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        head_id, tail_id = _build_chain(
            db, Node(name="n1"), Node2(name="n2"), Node(name="n3"), Node2(name="n4")
        )

    with Session(engine) as db:
        names, types = _traverse_forward(db, Node, head_id)
        assert names == ["n1", "n2", "n3", "n4"]
        assert types == ["Node", "Node2", "Node", "Node2"]

        assert _traverse_backward(db, Node, tail_id) == ["n4", "n3", "n2", "n1"]


def test_linked_list_single_jti_node():
    """Single jointed table inheritance node has no successor (mirrors test_two)."""
    Node, NodeB, Node2, Node3 = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        n = Node3(name="only")
        db.add(n)
        db.commit()
        nid = n.id

    with Session(engine) as db:
        n = db.get(Node, nid)
        assert isinstance(n, Node3)
        assert n.nxt is None
        assert n.related_id is None


def test_linked_list_all_four_subtypes():
    """Chain mixing all four subtypes traverses correctly (mirrors test_three)."""
    Node, NodeB, Node2, Node3 = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    chain = [
        Node2(name="a"),
        Node(name="b"),
        NodeB(name="c"),
        Node3(name="d"),
        Node3(name="e"),
        NodeB(name="f"),
        NodeB(name="g"),
        Node2(name="h"),
        Node(name="i"),
    ]
    expected_types = ["Node2", "Node", "NodeB", "Node3", "Node3", "NodeB", "NodeB", "Node2", "Node"]
    expected_names = list("abcdefghi")

    with Session(engine) as db:
        head_id, tail_id = _build_chain(db, *chain)

    with Session(engine) as db:
        names, types = _traverse_forward(db, Node, head_id)
        assert names == expected_names
        assert types == expected_types

        assert _traverse_backward(db, Node, tail_id) == list(reversed(expected_names))


def test_linked_list_sti_node_in_jti_chain():
    """Single table inheritance node (NodeB) appears correctly typed when retrieved via base class."""
    Node, NodeB, Node2, Node3 = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        head_id, _ = _build_chain(
            db, Node2(name="start"), NodeB(name="middle"), Node3(name="end")
        )

    with Session(engine) as db:
        head = db.get(Node, head_id)
        assert isinstance(head, Node2)
        assert isinstance(head.nxt, NodeB)
        assert isinstance(head.nxt.nxt, Node3)
